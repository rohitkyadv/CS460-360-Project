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
if len(argv) < 2:
    print("A sentence must be included")
    exit()

# Write sentence to file for logging
file = open("log.log", "a")
file.write("Time is: %s - %s\n" % (datetime.now(),  argv[1]))
file.close()

#-------------------------------------------------------------------------------
# Basic sentence parsing & tokenization
#-------------------------------------------------------------------------------

# echo the sentence
sentence = argv[1]
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
print ("Tree 1: ",tree)
print("\nTree 2: ", tree.pformat_latex_qtree())
print("\nPretty tree:\n")
tree.pretty_print()


#-------------------------------------------------------------------------------
# Build a schema of the database
#-------------------------------------------------------------------------------

#db = "drugsdatabase"
db = "world"

print ("\n--- Get all tables from database ---")
tables = db_run_querey(db, "SELECT table_name FROM information_schema.tables where table_schema='" + db + "';")

print ("\n--- Get attributes from all tables ---")
db_schema = {}
for t in tables:
    db_schema[t.lower()] = {}  # create dictionary of attributes
    #print (i)
    attributes = db_run_querey('information_schema', "SELECT column_name FROM `COLUMNS` where table_schema = '" + db + "' and table_name = '" + t + "'")
    for a in attributes:
        db_schema[t][a.lower()] = [a.lower()]
print ("------")
#print("Post table grab: %s" % db_schema)               # debugger
db_schema = alias_lookup(db_schema)
#print("-----\nPost table alias: %s" % db_schema)       # debugger


    
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
                print("return was: %s, len is: %s" % (rtn, len(rtn)))
                if (rtn != 0):
                    #output['SELECT'].extend(rtn)
                    output = addListToDic(output, 'SELECT', rtn)
                    print ("output: %s" % output['SELECT'])
    return output
            
        # height 2 is pos, height 1 is the word
        
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
    for i in L:
        if (len(dic[key]) == 0):
            dic[key] = L
        else:
            dic[key].extend(L)
            
    # print ("dic function: ", dic)     # debugger
    return dic

print ("--- Traversing the tree ---")
traverseTree(sql_output, db_schema, tree)


#-------------------------------------------------------------------------------
# build the querry
#-------------------------------------------------------------------------------

query = sql_output['SELECT'] + sql_output['FROM'] + sql_output['WHERE']
SELECT_L = sql_output['SELECT']
SELECT = ""


# SELECT clause
for idx, val in enumerate(SELECT_L):
    if (len(SELECT) == 0):
        SELECT += 'Select ' + val[0] + "." + val[1]
    else:
        
        SELECT += ', ' + val[0] + "." + val[1]
        
print (SELECT)

# FROM clause
#FROM_L = sql_output['FROM']
FROM_L = []
FROM_L.extend(SELECT_L)
FROM_L.extend(sql_output['WHERE'])
FROM = ""
for idx, val in enumerate(FROM_L):
    if (len(FROM) == 0):
        FROM += ' FROM ' + val[0] + "." + val[1]
    else:
        
        FROM += ' NATURAL JOIN ' + val[0]

# WHERE clause
WHERE_L = sql_output['FROM']
WHERE = ""
for idx, val in enumerate(WHERE_L):
    if (len(WHERE) == 0):
        WHERE += ' WHERE ' + val[0] + "." + val[1]
    else:
        
        WHERE += ', ' + val[0] + "." + val[1]


query = SELECT + FROM + WHERE + ";"
print("\nOutput Query: ", query)


#-------------------------------------------------------------------------------
# Run output SQL query
#exit()  # not ready yet
#-------------------------------------------------------------------------------

db_run_querey(db, query)


# end program