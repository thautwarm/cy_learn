from sklearn.feature_extraction.text import TfidfTransformer
from collections import Counter
from typing import List
from sklearn.feature_extraction import DictVectorizer
from nltk.tokenize import word_tokenize

import nltk
import numpy as np
import xython as xy
import pandas as pd
import string

Word = str
Doc = List[Word]
ReadOnly = property
_EmptySet = set()


class Word2Vec:
    def __init__(self, sparse=True, sort=True, use_tf_idf=True,
                 punctuation=set(string.punctuation),
                 stop_words=nltk.corpus.stopwords.words('english')):

        self.abandon = set.union(_EmptySet, *(each for each in (punctuation, stop_words) if each))
        if not self.abandon:
            self.abandon = None

        self.vectorizer = DictVectorizer(sparse=sparse, sort=sort)
        self.tf_idf = TfidfTransformer() if use_tf_idf else None
        self._fitted = False
        self._transform = None
        self._hold_data = None

    def fit(self, documents: List[Doc], hold_data=False):
        if self.abandon:
            documents = map | xy.partial(documents) | xy.call(
                lambda _: filter(lambda word: word not in self.abandon, _))

        data = [Counter(doc) for doc in documents]

        self.vectorizer.fit(data)

        if self.tf_idf:
            data = self.vectorizer.transform(data)
            self.tf_idf.fit(data)
            self._transform = xy.and_then(self.vectorizer.transform, self.tf_idf.transform)
        else:
            self._transform = self.vectorizer.transform
        if hold_data:
            self._hold_data = data
        self._fitted = True

    def transform(self, documents: List[Doc]):
        if not self.fitted:
            self.fit(documents, hold_data=True)
            data = self.tf_idf.transform(self._hold_data)
            del self._hold_data
            return data

        return self._transform([Counter(doc) for doc in documents])

    @ReadOnly
    def fitted(self):
        return self._fitted

    @ReadOnly
    def feature_names(self):
        return np.array(self.vectorizer.get_feature_names())


def counter(documents: List[Doc]):
    return [Counter(doc) for doc in documents]


if __name__ == '__main__':
    corpus = """The ACT originally consisted of four tests: English, Mathematics, Social Studies, and Natural Sciences. 
In 1989 however, the Social Studies test was changed into a Reading section (which included a Social Studies subsection) and the Natural Sciences test was renamed the Science Reasoning test, with more emphasis on problem solving skills.[12] 
In February 2005, an optional Writing test was added to the ACT, mirroring changes to the SAT that took place later in March of the same year. 
In 2013, ACT announced that students would be able to take the ACT by computer starting in the spring of 2015. The test will continue to be offered in the paper format for schools that are not ready to transition to computer testing.[13]
The ACT has seen a gradual increase in the number of test takers since its inception, and in 2011 the ACT surpassed the SAT for the first time in total test takers; that year, 1,666,017 students took the ACT and 1,664,479 students took the SAT.[14] 
All four-year colleges and universities in the U.S. accept the ACT,[15] but different institutions place different emphases on standardized tests such as the ACT, compared to other factors of evaluation such as class rank, GPA, and extracurricular activities.
""".splitlines()
    documents = [word_tokenize(doc) for doc in corpus]

    w2v = Word2Vec()
    print(pd.DataFrame(w2v.transform(documents).toarray(),
                       columns=w2v.feature_names))
