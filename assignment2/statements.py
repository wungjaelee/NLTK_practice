# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements
from collections import defaultdict

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    # add code here
    def __init__(self):
        self.pos_tag_to_stem= defaultdict(list)

    def add(self, stem, pos_tag):
        self.pos_tag_to_stem[pos_tag].append(stem)

    def getAll(self, target_pos_tag):
        return list(set(self.pos_tag_to_stem[target_pos_tag]))

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

#preprocess Brown Tagged Words
VB = set()
VBZ = set()
for word, tag in brown.tagged_words():
    if tag == 'VB':
        VB.add(word)
    elif tag == 'VBZ':
        VBZ.add(word)
    else:
        continue

def is_verb(s, stem):
    return s in VBZ or stem in VB

def stem(s):
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
        raise ValueError("Not in 3s form")


def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    # add code here

    # convert s to stem
    try:
        hypothesized_stem = stem(s)
    except ValueError:
        # s is not in 3s form
        return ""
    if is_verb(s, stem):
        return hypothesized_stem
    else:
        return ""


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
