import nltk
nltk.download('stopwords')

from sklearn.base import BaseEstimator, TransformerMixin
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

STOPWORDS = set(stopwords.words('english'))

class SelectAtribute(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None, *parg, **kwarg):
        return self
    
    def transform(self, X):
        return X[self.key]

class CleanTweets(BaseEstimator, TransformerMixin):
    def __init__(self, key):
        self.key = key

    def fit(self, X, y=None, *parg, **kwarg):
        return self
    
    def transform(self, X):
        preprocessed_tweets = []
        # tqdm is for printing the status bar
        for sentance in tqdm(X):
            sentance = re.sub(r'https?://\S+|www\.\S+', r'', sentance) # remove URLS
            sentance = re.sub(r'<.*?>', r'', sentance) # remove HTML
            sentance = BeautifulSoup(sentance, 'lxml').get_text()
            sentance = decontracted(sentance)
            sentance = re.sub(r'\d+', '', sentance).strip() # remove number
            sentance = re.sub(r"[^\w\s\d]","", sentance) # remove pnctuations
            sentance = re.sub(r'@\w+','', sentance) # remove mentions
            sentance = re.sub(r'#\w+','', sentance) # remove hash
            sentance = re.sub(r"\s+"," ", sentance).strip() # remove space
            sentance = re.sub("\S*\d\S*", "", sentance).strip()
            sentance = re.sub('[^A-Za-z]+', ' ', sentance)

            sentance = ' '.join([e.lower() for e in sentance.split() if e.lower() not in STOPWORDS])
            preprocessed_tweets.append(sentance.strip())
        return preprocessed_tweets
    
    def decontracted(phrase):
        # specific
        phrase = re.sub(r"won't", "will not", phrase)
        phrase = re.sub(r"can\'t", "can not", phrase)

        # general
        phrase = re.sub(r"n\'t", " not", phrase)
        phrase = re.sub(r"\'re", " are", phrase)
        phrase = re.sub(r"\'s", " is", phrase)
        phrase = re.sub(r"\'d", " would", phrase)
        phrase = re.sub(r"\'ll", " will", phrase)
        phrase = re.sub(r"\'t", " not", phrase)
        phrase = re.sub(r"\'ve", " have", phrase)
        phrase = re.sub(r"\'m", " am", phrase)
    return phrase