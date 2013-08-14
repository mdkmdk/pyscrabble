
import re
import sys
import timeit

f = open('/media/mk-data/Dropbox/PythonAnywhere/Scrabble/Wordlists/scrabbledict-0.91/sowpods.txt')

words = [lin for lin in f.readlines()]

    # remove the "\n" how ?
    
timeit.timeit(stmt="f = open('/media/mk-data/Dropbox/PythonAnywhere/Scrabble/Wordlists/scrabbledict-0.91/sowpods.txt');words = [lin for lin in f.readlines()];xyl_exists=[(i,w) for i,w in enumerate(words) if w.find('xyl') != -1]")

timeit.timeit()
srch_str = 'xyl'
for i,w in enumerate(words):
    if w.find(srch_str) != -1:
        print "Success"
        print w
        print i
        break
# finally:
#     print "Failure bro"
