# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?
tagset = set(["P", "A", "Ns", "Np", "Is", "Ip", "Ts", "Tp", "BEs", "BEp", "DOs", "DOp", "AR", "AND", "WHO", "WHICH", "?"])

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'),
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

#function_words = [p[0] for p in function_words_tags]
function_word_to_tag = dict(function_words_tags)

def unchanging_plurals():
    nn_words = set()
    nns_words = set()
    with open("sentences.txt", "r") as f:
        for line in f:
            # add code here
            for word_pos in line.split(" "):
                word, pos = word_pos.split("|")
                if pos == "NN":
                    nn_words.add(word)
                elif pos == "NNS":
                    nns_words.add(word)
    return intersection(nn_words, nns_words)

unchanging_plurals_set = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""
    # add code here
    if s in unchanging_plurals_set:
        return s
    elif s.endswith("men"):
        return s[:-3] + "man"
    else:
        try:
            return stem(s)
        except ValueError:
            #s not in 3s form or s does not match any 3s->stem rules
            return ""

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    # add code here
    tags = []
    hypothesized_verb_stem = verb_stem(wd)
    hypothesized_noun_stem = noun_stem(wd)

    #if s is verb plural
    if hypothesized_verb_stem:
        if hypothesized_verb_stem in lx.getAll('I'):
            tags.append('Ip')
        if hypothesized_verb_stem in lx.getAll('T'):
            tags.append('Tp')

    #if s is noun plural
    if hypothesized_noun_stem and hypothesized_noun_stem in lx.getAll('N'):
        tags.append('Np')

    # check if given word is a function_word
    try:
        tags.append(function_word_to_tag[wd])
    except KeyError:
        pass

    # lastly add any tags associated to given word in lexicon
    for lx_tag in ['P', 'N', 'A', 'I', 'T']:
        if wd in lx.getAll(lx_tag):
            if lx_tag == 'P' or lx_tag == 'A':
                tags.append(lx_tag)
            else:
                tags.append(lx_tag + 's')

    return tags





def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
