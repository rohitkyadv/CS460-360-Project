#!/usr/bin/python3
from sys import argv                # for arguments
from datetime import datetime       # for date printing
import nltk                         # natural language tookkit
import pymysql

print ("Time is: ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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
      'user': 'root',
      'passwd': None,
      'host': '127.0.0.1',
      'db': db,
    }
    try:
      conn = pymysql.connect(**config)
    except Exception as e:
        print ("error ", e)
        return 1
    else:
        cur = conn.cursor()
        cur.execute(query)
        for response in cur:
            #print("Response: %r\tType: %r" % (response, type(response)))   # response is a tuple
            print(response)
        cur.close()
        conn.close()
        
db = "phpteset"
db_run_querey(db, "show tables")
print ("....")
db_run_querey(db, "select * from MarketingStatus")