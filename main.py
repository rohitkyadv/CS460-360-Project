#!/usr/bin/python3
from sys import argv                # for arguments
from datetime import datetime       # for date printing
import nltk                         # natural language tookkit
from stat_parser import Parser, display_tree    # https://stackoverflow.com/a/17935542
from nltk.corpus import treebank
from nltk import Tree
import pymysql
from lib_alias import alias_lookup

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


# echo the sentence
sentence = argv[1]
print ("Sentence is: %s" % sentence)

# separates sentence into tokens or individual words
tokens = nltk.word_tokenize(sentence)
print ("\nTokens %r\n" % tokens)

# identifies each token to a part of speech
tagged = nltk.pos_tag(tokens)
print ("Tagged words: %r\n" % tagged)


parser = Parser()
# http://www.thrivenotes.com/the-last-question/
#sentance = "What is the population of the country France?"
tree = parser.parse(sentence)
print ("--- Printing trees -----")
print ("Tree 1: ",tree)
print("\nTree 2: ", tree.pformat_latex_qtree())
print("\nPretty tree:\n")
tree.pretty_print()

print ("--- Looking through the tree -----")
print (tree[1])
print (type(tree[1]))
x = tree[1][1]
print ("val: %s, type: %s" % (x, type(x)))
print (len(x))
print (len(tree))
print (tree.label())
print (tree[0].label())
print (tree[0][0].label())

print (len(tree[0][0]))
print (len(tree[0][0][0]))
print (tree[0][0][0])

print(tree[0].leaves())
print(tree[1].leaves())



# this runs a database querey and returns a list of what was returned.
def db_run_querey(db, query):
    # https://stackoverflow.com/a/13846183
    config = {
      'user': 'nick',
      'passwd': 'harvey',
      'host': 'database.nkren.net',
      'db': db,
    }
    try:
      conn = pymysql.connect(**config)
    except Exception as e:
        print ("error ", e)
        return 1
    else:
        cur = conn.cursor()
        try:
            cur.execute(query)
        except Exception as e:
            print("An error occured when executing query")
            print("\tThe query: %r " % query)
            print (e)
            return 1
        else:
            rtn_list = []
            #print (cur.fetchall())
            for response in cur:
                #print("Response: %r\tType: %r" % (response, type(response)))   # response is a tuple
                print(response)
                rtn_list.append(response[0])
            #print ("rtn_list: %r" % rtn_list)
        cur.close()
        conn.close()
    return rtn_list


# this function takes a keyword and finds that keyword in the database schema.
# if a hit is found, this function returns a list of tuples for each match [(table, column), (table, column)]
def find_attribute(keyword, schema):
    keyword = keyword.lower()
    # is keyword a table?
    #if keyword in schema:
    #    print("%s is a table name" % keyword)
    
    # is keyword a attribute of a table
    match_found = False
    rtn_list = []
    for t in schema:                            # loop through tables
        #print ("table: %s" % t)                # debugger
        for a in schema[t]:                     # search attributes in table
            #print ("  attribute: %s" % a)      # debugger
            if keyword in schema[t][a]:         # test if keyword exits in the list of aliases for a given attribute
                #print("Found match for %s in table %s, column: %s" % (keyword, t, a))      # debugger
                match_found = True
                rtn_list.append((t,a))          # add result tuple to return list
    if not match_found:
        print ("No match found for %s" % keyword)
        return 0
    #print("\n>>" + keyword + ": " + str(rtn_list))
    return rtn_list

# SQL reference queries
# SELECT TABLE_SCHEMA, TABLE_NAME FROM information_schema.tables where table_schema='drugsdatabase';
# SELECT table_name, column_name FROM `COLUMNS` where table_schema = 'drugsdatabase' and table_name = 'marketingstatus'
# SELECT table_name, column_name FROM `COLUMNS` where table_schema = 'drugsdatabase'





# SELECT
# FROM
# WHERE
sql_output = {}
sql_output['SELECT'] = ""
sql_output['FROM']   = ""
sql_output['WHERE']  = ""


# build a schema of the database
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
#print("Post table grab: %s" % db_schema)       # debugger
db_schema = alias_lookup(db_schema)
#print("-----\nPost table alias: %s" % db_schema)       # debugger



# Examples of finding keywords in our database
print ("\n--- Examples of keword lookups ---")
g = find_attribute("Capital", db_schema)
print ("Capital  %s"%g)
g = find_attribute("Language", db_schema)
print ("Language  %s"%g)
g = find_attribute("City", db_schema)
print ("City  %s"%g)
g = find_attribute("Town", db_schema)
print ("Town  %s"%g)
g =find_attribute("Population", db_schema)
print ("Population  %s"%g)
g =find_attribute("Size", db_schema)
print ("Size  %s"%g)
g = find_attribute("Strength", db_schema)
print ("Strength  %s"%g)


exit()  # not ready yet
# Run output SQL query
db_run_querey(db, sql_output['SELECT'] + sql_output['FROM'] + sql_output['WHERE'])






exit()
db_schema_example = { 
            "Table1" :
              {
                  "Movies": ["Movies", "Films", "Film"],
                  "c2": ["c2", "a1", "a2"],
                  "c3": ["c3"],
                  "c4": ["c4"]
              },
            "Table2" : ["c1", "a1", "a2"]
            }
