#!/usr/bin/python3
from sys import argv                # for arguments
from datetime import datetime       # for date printing
import nltk                         # natural language tookkit

print ("Time is: ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
 # we use <br> for new lines since this is generating html content for php
print ("<br>")

#print "\nArg1: ", argv[1:]  # Will print out all arguments starting at 1
#print "<br>"

# echo the sentence
sentence = argv[1]
#sentence = """At eight o'clock on Thursday morning"""   # debugging
print ("Sentence is: %s" % sentence)
print ("<br>")

# separates sentence into tokens or individual words
tokens = nltk.word_tokenize(sentence)
print ("\nTokens %r\n" % tokens)
print ("<br>")

# identifies each token to a part of speech
tagged = nltk.pos_tag(tokens)
print ("Tagged words: %r\n" % tagged[0:6])
