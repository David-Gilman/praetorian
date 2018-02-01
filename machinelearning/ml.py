from io import StringIO
import numpy as np
import binascii
import requests
import logging
import base64
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB


data = []
target = []


class Server(object):
    url = 'https://mlb.praetorian.com'
    log = logging.getLogger(__name__)

    def __init__(self):
        self.session = requests.session()
        self.binary  = None
        self.hash    = None
        self.wins    = 0
        self.targets = []

    def _request(self, route, method='get', data=None):
        while True:
            try:
                if method == 'get':
                    r = self.session.get(self.url + route)
                else:
                    r = self.session.post(self.url + route, data=data)
                if r.status_code == 429:
                    raise Exception('Rate Limit Exception')
                if r.status_code == 500:
                    raise Exception('Unknown Server Exception')

                return r.json()
            except Exception as e:
                self.log.error(e)
                self.log.info('Waiting 60 seconds before next request')
                time.sleep(60)

    def get(self):
        r = self._request("/challenge")
        self.targets = r.get('target', [])
        self.binary = base64.b64decode(r.get('binary', ''))
        return r

    def post(self, target):
        r = self._request("/solve", method="post", data={"target": target})
        self.wins = r.get('correct', 0)
        self.hash = r.get('hash', self.hash)
        self.ans  = r.get('target', 'unknown')
        return r


def read_in():
    f = open("dataset10000.dat.txt", "r")

    for line in f:
        line = line.split(':')
        target.append(line[0])
        data.append(line[1].encode('utf-8').hex())


if __name__ == '__main__':
    read_in()
    vec_opts = {
        "ngram_range": (1, 4),  # allow n-grams of 1-4 words in length (32-bits)
        "analyzer": "word",  # analyze hex words
        "token_pattern": "..",  # treat two characters as a word (
        #"max_df": 1.0,
        "min_df": .001
    }

    idf_opts = {"use_idf": True}
    idf = TfidfTransformer(**idf_opts)

    pipeline = Pipeline([
        ('vec', CountVectorizer(**vec_opts)),
        ('idf', TfidfTransformer(**idf_opts)),
        #('clf', MultinomialNB())
    ])

    X = pipeline.fit_transform(data, target)
    mnb = MultinomialNB().fit(X, target)

    s = Server()

    while True:
        s.get()

        bin = s.binary.hex()

        xtest = pipeline.transform([bin])
        target = mnb.predict(xtest)
        #target = X.predict([s.binary.hex()])

        s.post(target)

        print("Guess: " + str(target) + " Answer: " + str(s.ans) + " Wins: " + str(s.wins))
        #s.log.info("Guess:[{: >9}]   Answer:[{: >9}]   Wins:[{: >3}]".format(str(target), s.ans, s.wins))


        if s.hash:
            s.log.info("You win! {}".format(s.hash))