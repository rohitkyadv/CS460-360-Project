#!/usr/bin/python3
from sys import argv                # for arguments
from datetime import datetime       # for date printing
import nltk                         # natural language tookkit
from stat_parser import Parser, display_tree    # https://stackoverflow.com/a/17935542
from nltk.corpus import treebank
from nltk import Tree
from lib_alias import alias_lookup
from lib_sql_db import db_run_querey, find_attribute

# print current time to file to prove we ran
print (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#print "\nArg1: ", argv[1:]  # Will print out all arguments starting at 1
if len(argv) < 3:
    print("A db and sentence must be included")
    exit()

# Write sentence to file for logging
file = open("log.log", "a")
file.write("Time is: %s - %s\n" % (datetime.now(),  argv[1]))
file.close()

#-------------------------------------------------------------------------------
# Basic sentence parsing & tokenization
#-------------------------------------------------------------------------------
# echo the sentence
sentence = argv[2]
print ("Sentence is: %s" % sentence)

# separates sentence into tokens or individual words
tokens = nltk.word_tokenize(sentence)
print ("\nTokens %r\n" % tokens)

# identifies each token to a part of speech
tagged = nltk.pos_tag(tokens)
print ("Tagged words: %r\n" % tagged)


#-------------------------------------------------------------------------------
# Generate nltk tree
#-------------------------------------------------------------------------------

parser = Parser()
# http://www.thrivenotes.com/the-last-question/
#sentance = "What is the population of the country France?"
tree = parser.parse(sentence)
print ("--- Printing trees -----")
#print ("Tree 1: ",tree)
#print("\nTree 2: ", tree.pformat_latex_qtree())
#print("\nPretty tree:\n")
tree.pretty_print()


#-------------------------------------------------------------------------------
# Build a schema of the database
#-------------------------------------------------------------------------------

db = argv[1]
#db = "drugsdatabase"
#db = "Genes_Proteins"
if not (db == "world" or db == "drugsdatabase" or db == "Genes_Proteins"):
    print ("%r not a authorized database." % db)
    exit(1)
print ("Using database: %s" % db)

#print ("\n--- Get all tables from database ---")
tables = db_run_querey(db, "SELECT table_name FROM information_schema.tables where table_schema='" + db + "';")
#print ("\n--- Get attributes from all tables ---")
db_schema = {}
for t in tables:
    db_schema[t[0]] = {}  # create dictionary of attributes
    #print (i)
    attributes = db_run_querey('information_schema', "SELECT column_name FROM `COLUMNS` where table_schema = '" + db + "' and table_name = '" + t[0] + "'")
    for a in attributes:
        db_schema[t[0]][a[0]] = [a[0]]
#print ("------")
#print("Post table grab: %s" % db_schema)               # debugger
db_schema = alias_lookup(db_schema)
#print("-----\nPost table alias: %s" % db_schema)       # debugger

# Test debugging
#find_attribute('Name', db_schema)
#find_attribute('language', db_schema)

#exit()
#-------------------------------------------------------------------------------
# Traverse the tree
#-------------------------------------------------------------------------------

# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
def traverseTree(output, db_schema, tree):
    print("Pre output: ", output)
    tree_len = len(tree)
    tree_height = tree.height()
    print ("Lable: %s    Len: %d   Height: %d    Leaves: %s" % (tree.label(), tree_len, tree.height(), tree.leaves()))
    tree.pretty_print()
    
    # Look at every branch on the tree
    for i in range(tree_len):
        print ("i: ", i)
        if tree_height >2:
            pos = tree.label()
            #if pos == "NP":
                #if (tree[0] == "DT")
                    # add to select
            
            # peak ahead to see if it's a D if so 
            output_rtn = traverseTree(output, db_schema, tree[i])
            #if (output_rtn != 0 and type(output_rtn) > 0):
            print("output_rtn: ", output_rtn)
            output = output_rtn
        else:
            pos = tree.label()
            word = tree[0]
            print ("## word is: %s,  pos is: %s" % (word, pos))
            if pos == 'NN':
                rtn = find_attribute(word, db_schema)
                if (rtn != 0):
                    print("return was: %s, len is: %s" % (rtn, len(rtn)))
                    #output['SELECT'].extend(rtn)
                    output = addListToDic(output, 'SELECT', rtn)
                    print ("output: %s" % output['SELECT'])
    return output
            
        # height 2 is pos, height 1 is the word
        
        
        
def traverseTree2(output, db_schema, tagged):
    #print (tagged)
    state = None
    where_tbls = []
    where_conds = []
    for idx, val in enumerate(tagged):
        #print ("idx: %d, val: %s, \tstate: %s" % (idx, val, state))
        if state == 'selecting':
            if  val [1][0:2] == 'NN':
                rtn = find_attribute(val[0], db_schema)
                #print ('rtn ', rtn)
                if not rtn == 0:
                    output['SELECT'].extend(rtn)
                
                #peak ahead
                if idx + 1 < len(tagged):
                    if not tagged[idx+1][1] == "CC" and not tagged[idx+1][1] == ",":
                        state = None
            elif val[1] == 'CC':
                continue
            
            
        elif state == 'where':
            #print("where")
            if val[1][0:2] == 'DT':
                state = 'where-att'
                continue
            elif  val [1][0:2] == 'NN':
                rtn = find_attribute(val[0], db_schema)
                #print ('rtn ', rtn)
                if not rtn == 0:
                    output['SELECT'].extend(rtn)
                
                #peak ahead
                if idx + 1 < len(tagged):
                    if not tagged[idx+1][1] == "CC" and not tagged[idx+1][1] == ",":
                        state = None
            if val[1] == 'CC':
                continue
        
        elif state == 'where-att':
            #print ("where-att")
            if val [1][0:2] == 'NN':
                rtn = find_attribute(val[0], db_schema)
                #print ('rtn ', rtn)
                if not rtn == 0:
                    where_tbls.extend(rtn)
                    #print ("output where ", output['WHERE'])
                else:
                    print ("## potential sentence format error")
                    continue
                #peak ahead
                if idx + 1 < len(tagged):
                    if tagged[idx+1][1] == "CC":
                        continue
                    if tagged[idx+1][1][0:2] == 'NN':
                        state = 'where-cond'
                    else:
                        print ("## potential sentence format error")
                        state = None
                        
        elif state == 'where-cond':
            #print ("where-att")
            if val [1][0:2] == 'NN':
                # condition value
                where_conds.append(val[0])
                
                #peak ahead
                if idx + 1 < len(tagged):
                    if tagged[idx+1][1] == "CC" or tagged[idx+1][1] == ",":
                        continue
                    else:
                        state = None
                    

        elif (val[1][0:2] == 'DT'):
            state = 'selecting'
        elif (val[1][0:2] == 'IN' or val[1].lower() == 'where'):
            state = 'where'
    
    #print("---\npost where lists")
    #print (where_tbls)
    #print (where_conds)
    
    # combine lists
    whereoutput  = ""
    for att in where_tbls:
        for cond in where_conds:
            if len(whereoutput ) == 0:
                whereoutput  += ' WHERE ' + att[0] + '.' + att[1] + '="' + cond + '"'
            else:
                whereoutput  += ' or ' + att[0] + '.' + att[1] + '="' + cond + '"'
                
    #print ("post where combine: ", whereoutput )
    output['WHERE'] = whereoutput 
    
    
    
    
# SELECT
# FROM
# WHERE
sql_output = {}
sql_output['SELECT'] = []
sql_output['FROM']   = []
sql_output['WHERE']  = []

attributes = []

# give a dictionary and key then append list items as such x | x | x | x
def addListToDic(dic, key, L):
    # print ("add2L: dic: %s,   L: %s" % (dic, L))  # debugger
    for i in L:
        dic[key].extend(L)
            
    # print ("dic function: ", dic)                 # debugger
    return dic

#print ("--- Traversing the tree ---")
#traverseTree(sql_output, db_schema, tree)
traverseTree2(sql_output, db_schema, tagged)

#-------------------------------------------------------------------------------
# build the querry
#-------------------------------------------------------------------------------

print ("\n\n--- Building the querry ---")
#print ("Query data: ", sql_output)
SELECT_L = sql_output['SELECT']
SELECT = ""
# SELECT clause
for idx, val in enumerate(SELECT_L):
    if (len(SELECT) == 0):
        SELECT += 'Select ' + val[0] + "." + val[1]
    else:
        SELECT += ', ' + val[0] + "." + val[1]


# FROM clause
#FROM_L = sql_output['FROM']
FROM_L = []
FROM_L.extend(SELECT_L)
#FROM_L.extend(sql_output['WHERE'])
FROM_Added = []                             # contains unique list of tables we've added
FROM = ""
for idx, val in enumerate(FROM_L):
    if (len(FROM) == 0):                    # if empty
        FROM += ' FROM ' + val[0]
        FROM_Added.append(val[0])           # add first to unique list
    else:
        if (val[0] not in FROM_Added):      # test if we've already added this table before
            FROM += ' NATURAL JOIN ' + val[0]
            FROM_Added.append(val[0])       # Add item to unique list

# WHERE clause
WHERE_L = sql_output['FROM']
WHERE = ""
for idx, val in enumerate(WHERE_L):
    if (len(WHERE) == 0):
        WHERE += ' WHERE ' + val[0] + "." + val[1]
    else:
        
        WHERE += ', ' + val[0] + "." + val[1]

print ("Select: %r" % SELECT)
print ("From:   %r" % FROM)
#print ("Where:  %r" % WHERE)
print ("Where:  %r" % sql_output['WHERE'])
query = SELECT + FROM + sql_output['WHERE'] + " LIMIT 15;"
print("\nOutput Query: ", query)


#-------------------------------------------------------------------------------
# Run output SQL query
#-------------------------------------------------------------------------------
print ("\n" +SELECT_L[0][1], end='')
del SELECT_L[0]         # delete first item
for header in SELECT_L:
    print (", ", header[1], end='')
print()
output = db_run_querey(db, query)
for i, r in enumerate(output):
    for i, e in enumerate(r):
        print ("%s\t" % str(e), end='')
    print()

# end program
