# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    # add code here
    def __init__(self):
        self.stemCatPairs= []

    def add(self, stem, cat):
        self.stemCatPairs.append((stem, cat))

    def getAll(self, targetCategory):
        return list(set([stem for stem, cat in self.stemCatPairs if cat == targetCategory]))

class FactBase:
    """stores unary and binary relational facts"""
    # add code here
    def __init__(self):
        """
        some consideration
        lookup time: ?
        allow duplicate: ?
        """
        self.unaryFacts = set()
        self.binaryFacts = set()

    def addUnary(self, pred, e1):
        self.unaryFacts.add((pred, e1))

    def queryUnary(self, pred, e1):
        return (pred, e1) in self.unaryFacts

    def addBinary(self, pred, e1, e2):
        self.binaryFacts.add((pred, e1, e2))

    def queryBinary(self, pred, e1, e2):
        return (pred, e1, e2) in self.binaryFacts

import re
from nltk.corpus import brown
def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    # add code here
    if re.match(r'.*[^sxyzaeiou]s$', s):
        #Need to figure out how to include ch, sh
        print("case1: ", s)
        return s[:-1]
    elif re.match(r'.*[aeiou]ys$', s):
        print("case2: ", s)
        return s[:-1]
    elif re.match(r'.+[^aeiou]ies$', s):
        print("case3: ", s)
        return s[:-3] + "y"
    elif re.match(r'[^aeiou]ies$', s):
        print("case4: ", s)
        return s[:-1]
    elif re.match(r'.*(o|x|ch|sh|ss|zz)es$', s):
        print("case5: ", s)
        return s[:-2]
    elif re.match(r'.*([^s]se|[^z]ze)s$', s):
        print("case6: ", s)
        return s[:-1]
    elif s == 'has':
        print("case7: ", s)
        return 'have'
    elif re.match(r'.*(?![iosxz]|ch|sh)es$', s):
        #probably not the way to do this
        #look into how to except not just a character but also string
        print("case8: ", s)
        return s[:-1]
    else:
        return s


def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg

# End of PART A.
