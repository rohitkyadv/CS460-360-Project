#!/usr/bin/python3
from sys import argv                # for arguments
from datetime import datetime       # for date printing
import nltk                         # natural language tookkit
import pymysql

print ("Time is: ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
if len(argv) < 2:
    print("Missing arguments")
    exit()

# print current time to file to prove we ran
file = open("log.log", "a")
file.write("Time is: %s - %s\n" % (datetime.now(),  argv[1]))
file.close()

#print "\nArg1: ", argv[1:]  # Will print out all arguments starting at 1

# echo the sentence
sentence = argv[1]
#sentence = """At eight o'clock on Thursday morning"""   # debugging
print ("Sentence is: %s" % sentence)

# separates sentence into tokens or individual words
tokens = nltk.word_tokenize(sentence)
print ("\nTokens %r\n" % tokens)

# identifies each token to a part of speech
tagged = nltk.pos_tag(tokens)
print ("Tagged words: %r\n" % tagged[0:6])




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
        else:
            for response in cur:
                #print("Response: %r\tType: %r" % (response, type(response)))   # response is a tuple
                print(response)
        cur.close()
        conn.close()
        
db = "drugsdatabase"
db_run_querey(db, "show tables")
print ("....")
db_run_querey(db, "select * from MarketingStatus")
print("...")

#db_run_querey(db, "USE DBName GO SELECT * FROM sys.Tables GO")
db_run_querey(db, "SELECT table_name FROM information_schema.tables where table_schema='phpteset';")
print ("------")
db_run_querey(db, "SELECT column_name FROM information_schema.tables where table_schema='phpteset';")

db="information_schema"
query= "SELECT table_name, column_name FROM `COLUMNS` where table_schema = 'phpteset' and table_name = 'MarketingStatus'"
print ("\n" +query)
db_run_querey(db,query)


db_schema = { 
            "Table1" :
              {
                  "Movies": ["Movies", "Films", "Film"],
                  "c2": ["c2", "a1", "a2"],
                  "c3": ["c3"],
                  "c4": ["c4"]
              },
            "Table2" : ["c1", "a1", "a2"]
            }


print ("\n\n")
print (db_schema)