import nltk
from nltk.corpus.reader import CategorizedPlaintextCorpusReader

FPSPS = ["i", "my", "me"]


def build_cover_letter_corpus():
    return CategorizedPlaintextCorpusReader('./cover_letters', '.*', cat_file='categories.txt')

def draw_fpsps_dispersion_plot(cv_corpus, fileid):
    file_text = normalize(cv_corpus.words(fileid))
    nltk.draw.dispersion.dispersion_plot(file_text, FPSPS, ignore_case=True, title=fileid)

def print_corpus_info(cv_corpus):
    print('fileids: ', cv_corpus.fileids())
    print('categories: ', cv_corpus.categories())

def build_categories_fpsps_cfd(cv_corpus):
    return nltk.ConditionalFreqDist((cat, w.lower()) for cat in cv_corpus.categories() for w in cv_corpus.words(categories=cat) if w.lower() in FPSPS)

def build_files_fpsps_cfd(cv_corpus):
    return nltk.ConditionalFreqDist((fileid.split('.')[0], w.lower()) for fileid in cv_corpus.fileids() for w in cv_corpus.words(fileid) if w.lower() in FPSPS)

def word_percentage(target_word, nltk_text_obj):
    try:
        return 100 * nltk_text_obj.count(target_word) / len(nltk_text_obj)
    except ZeroDivisionError:
        return "NA"

def normalize(words):
    return [w.lower() for w in words]

def extract_job_titles_from_file_ids(fileids):
    return [fileid.split('.')[0] for fileid in fileids]


def main():
    cover_letter_corpus = build_cover_letter_corpus()

    #show fpsps dispersion
    #draw_fpsps_dispersion_plot(cover_letter_corpus, 'academic-advisor.txt')

    #build ConditionalFreqDist
    cfd_cat = build_categories_fpsps_cfd(cover_letter_corpus)
    cfd_file = build_files_fpsps_cfd(cover_letter_corpus)


    #tabulate cfd
    cfd_cat.tabulate(conditions=cover_letter_corpus.categories()[:10])
    cfd_file.tabulate(conditions=extract_job_titles_from_file_ids(cover_letter_corpus.fileids()[:10]))
    print()


    #fpsp percentages for each file and category
    print("category\tI\tmy\tme")
    for category in cover_letter_corpus.categories()[:10]:
        nltk_text_obj = nltk.Text(normalize(cover_letter_corpus.words(categories=category)))
        #print(len(nltk_text_obj))
        print(category + '\t' + '\t'.join([str(word_percentage(fpsp, nltk_text_obj)) for fpsp in FPSPS]))

    print()
    print("job_title\tI\tmy\tme")
    for fileid in cover_letter_corpus.fileids()[:10]:
        nltk_text_obj = nltk.Text(normalize(cover_letter_corpus.words(fileids=fileid)))
        print(fileid + '\t' + '\t'.join([str(word_percentage(fpsp, nltk_text_obj)) for fpsp in FPSPS]))



if __name__ == "__main__":
    main()




#fdist = nltk.FreqDist(psps)
#print(fdist.most_common(50))
#print(fdist.N())
#fdist.plot()

#cv_corpus = CategorizedPlaintextCorpusReader('./cover_letters', '.*', cat_file='categories.txt')
#cfd_cat = nltk.ConditionalFreqDist((cat, w.lower()) for cat in cv_corpus.categories() for w in cv_corpus.words(categories=cat) if w.lower() in fpsps_lower)
#cfd_file = nltk.ConditionalFreqDist((fileid.split('.')[0], w.lower()) for fileid in cv_corpus.fileids() for w in cv_corpus.words(fileid) if w.lower() in fpsps_lower)
#cfd = nltk.ConditionalFreqDist((w, fileid.split('.')[0]) for fileid in cv_corpus.fileids() for w in cv_corpus.words(fileid) if w.lower() in fpsps_lower)
#cfd.plot()
#cfd.tabulate()
