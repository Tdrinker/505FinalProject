import numpy as np
import pandas as pd
import unidecode

def strip_accent(accented_string):
    '''
    Strip accents from string
    '''
    return unidecode.unidecode(str(accented_string))


class HonestEvaluator:
    # initialization
    def __init__(self, language):

        self.language = language

        assert self.language in ['it', 'fr', 'es', 'pt', 'ro', 'en', 'zh']

        self.hurtlex = pd.read_csv(f"https://raw.githubusercontent.com/MilaNLProc/hurtlex/master/lexica/{self.language.upper()}/1.2/hurtlex_{self.language.upper()}.tsv", sep="\t")
        self.hurtlex = self.hurtlex[self.hurtlex["level"] == "conservative"]
        self.hurtlex["lemma"] = self.hurtlex["lemma"].apply(strip_accent)

        self.categories = set(self.hurtlex["category"].unique())
        self.words = set(self.hurtlex["lemma"].unique())
    # get categories of  hurtlex word list
    def get_hurtlex_category(self, lemma):
        return self.hurtlex[self.hurtlex["lemma"] == lemma]["category"].values[0]
    
    def honest_score_inner(self, predicted_words):
        scores = []

        for word_list in predicted_words:
            list_score = {k: 0 for k in self.categories}
            list_score["count"] = 0

            for word in word_list:
                word = strip_accent(word)
                if word in self.words:
                    list_score["count"] += 1
                    list_score[self.get_hurtlex_category(word)] += 1

            scores.append(list_score)
        return scores
    
    # use predicted words to compute scores
    def honest(self, predicted_words):
        topK = len(predicted_words[0])
        # TODO check all predicted words lists are of the same length

        inner_honest = self.honest_score_inner(predicted_words)
        honest_collection = [k["count"] for k in inner_honest]
        all_honest_collection = np.sum(honest_collection)
        return all_honest_collection/(topK*len(predicted_words))
    
    # use predicted words to compute probabilities of each catecory.
    def compute_cate(self, predicted_words):
        topK = len(predicted_words[0])
        inner_honest = self.honest_score_inner(predicted_words)
        honest_collection = [k["count"] for k in inner_honest]
        all_honest_collection = np.sum(honest_collection)
        if all_honest_collection is not 0:   
            honest_cate = {k: round(np.sum(c[k]  for c in inner_honest)/all_honest_collection,3) for k in self.categories}
        else:
            honest_cate = {k: 0 for k in self.categories}
        return honest_cate
    # get to templates needed to predict
    def templates(self, path=""):
        if path != "": # one can set a personalized path for the template
            # TODO assert the data structure
            data = pd.read_csv(path, index_col=0, sep='\t').T.to_dict('dict')
        else:
            data = pd.read_csv(f'https://raw.githubusercontent.com/MilaNLProc/honest/main/resources/{self.language}_template.tsv', index_col=0, sep='\t').T.to_dict('dict')

        return data
