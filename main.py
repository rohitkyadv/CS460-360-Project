#!/usr/bin/python3
import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')


from sys import argv                # for arguments
from datetime import datetime       # for date printing
import nltk                         # natural language tookkit

print ("Time is: ", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
# print current time to file to prove we ran

# Test if argv[1] is not null
if len(argv) < 2:
    print("A sentence must be included")
    exit()

file = open("log.log", "a")
file.write("Time is: %s - %s\n" % (datetime.now(),  argv[1]))
file.close()

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
print ("Tagged words: %r\n" % tagged)



print ("<br>")
print ("tag1: ", tagged[1])
#print ("tag2: ", tagged[2])
#print ("tag3: ", tagged[3])
#print ("tag4: ", tagged[4])
#print ("tag5: ", tagged[5])

from nltk.corpus import treebank
t = treebank.parsed_sents('wsj_0001.mrg')[0]
#t.draw()


from nltk import Tree




dp1 = Tree('dp', [Tree('d', ['the']), Tree('np', ['dog'])])
dp2 = Tree('dp', [Tree('d', ['the']), Tree('np', ['cat'])])
vp = Tree('vp', [Tree('v', ['chased']), dp2])
tree = Tree('s', [dp1, vp])
print(tree)

print(tree.pformat_latex_qtree())
tree.pretty_print()


sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
parser = nltk.ChartParser(groucho_grammar)
for tree in parser.parse(sent):
    print(tree)
