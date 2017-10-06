#!/usr/bin/python
import sys
from datetime import datetime
import nltk
print "Time is: ", datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print "<br>"
#print "\nArg1: ", sys.argv[1:]
#print "<br>"

sentence = sys.argv[1]
print "Sentence is: %s" % sentence
print "<br>"
#sentence = """At eight o'clock on Thursday morning"""
tokens = nltk.word_tokenize(sentence)
print ("\nTokens %r\n" % tokens)
print "<br>"
tagged = nltk.pos_tag(tokens)
print ("Tagged words: %r\n" % tagged[0:6])