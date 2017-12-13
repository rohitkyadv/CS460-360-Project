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
#print("Post table grab: %s" % db_schema)               # debugger
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



if False:
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
    
    
def traverseTree(tree):
    tree_len = len(tree)
    tree_height = tree.height()
    print ("Lable: %s    Len: %d   Height: %d    Leaves: %s" % (tree.label(), tree_len, tree.height(), tree.leaves()))
    tree.pretty_print()
    for i in range(tree_len):
        print ("i: ", i)
        if tree_height >2:
            traverseTree(tree[i])
        # height 2 is pos, height 1 is the word
        
# SELECT
# FROM
# WHERE
sql_output = {}
sql_output['SELECT'] = ""
sql_output['FROM']   = ""
sql_output['WHERE']  = ""

print ("--- Traversing the tree ---")
traverseTree(tree)




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
