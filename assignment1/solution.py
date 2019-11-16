import nltk
from nltk.corpus.reader import CategorizedPlaintextCorpusReader

fpsps = ["I", "me", "my"]
fpsps_lower = ["i", "me", "my"]

raw = open('/Users/wungjaelee/Documents/Squareteams/assignment1/cover_letters/academic-advisor.txt').read()

words = nltk.word_tokenize(raw)
#normalize words using lower()
words = [word.lower() for word in words]

text = nltk.Text(words)

psps = [word for word in words if word in fpsps_lower]

#count how many words are in the cover letter
print(len(words))
#count how many psps in the cover letter
print(psps)
#draw dispersion plot of psps in cover letter
#text.dispersion_plot(first_person_singular_pronouns, ignore_case=True)
#nltk.draw.dispersion.dispersion_plot(text, first_person_singular_pronouns, ignore_case=True)


fdist = nltk.FreqDist(psps)
print(fdist.most_common(50))
print(fdist.N())
#fdist.plot()

cv_corpus = CategorizedPlaintextCorpusReader('./cover_letters', '.*', cat_file='categories.txt')
cfd_cat = nltk.ConditionalFreqDist((cat, w.lower()) for cat in cv_corpus.categories() for w in cv_corpus.words(categories=cat) if w.lower() in fpsps_lower)
cfd_file = nltk.ConditionalFreqDist((fileid.split('.')[0], w.lower()) for fileid in cv_corpus.fileids() for w in cv_corpus.words(fileid) if w.lower() in fpsps_lower)
#cfd = nltk.ConditionalFreqDist((w, fileid.split('.')[0]) for fileid in cv_corpus.fileids() for w in cv_corpus.words(fileid) if w.lower() in fpsps_lower)
#cfd.plot()
#cfd.tabulate()
