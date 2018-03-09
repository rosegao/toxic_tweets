# Author: Rose Gao
# Project: Toxic Tweets

import pandas as pd
import numpy as np
import pickle

from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from scipy.sparse import hstack


class LemmaTokenizer(object):
    '''
    Tokenizer and lemmatizer using NLTK
    Code adapted from: http://scikit-learn.org/stable/modules/feature_extraction.html#customizing-the-vectorizer-classes
    '''
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


# create TFIDF vectorizers
def create_vectorizers(toxic_data):
    all_text = toxic_data['comment_text']

    word_vectorizer = TfidfVectorizer(
        sublinear_tf=True,
        strip_accents='unicode',
        tokenizer=LemmaTokenizer(),
        analyzer='word',
        token_pattern=r'\w{1,}',
        stop_words='english',
        ngram_range=(1, 1),
        max_features=10000)
    word_vectorizer.fit(all_text)

    # save vectorizer into a pickle file
    pickle.dump(word_vectorizer, open('toxicity_models/word_vectorizer.pickle', 'wb'))

    char_vectorizer = TfidfVectorizer(
        sublinear_tf=True,
        strip_accents='unicode',
        analyzer='char',
        stop_words='english',
        ngram_range=(2, 6),
        max_features=50000)
    char_vectorizer.fit(all_text)

    # save vectorizer into a pickle file
    pickle.dump(char_vectorizer, open('toxicity_models/char_vectorizer.pickle', 'wb'))


def feature_creation(toxic_data):
    '''
    Create train and test features
    '''
    word_vectorizer = pickle.load(open('toxicity_models/word_vectorizer.pickle', 'rb'))
    char_vectorizer = pickle.load(open('toxicity_models/char_vectorizer.pickle', 'rb'))

    word_features = word_vectorizer.transform(toxic_data['comment_text'])
    char_features = char_vectorizer.transform(toxic_data['comment_text'])
    features = hstack([char_features, word_features])

    return features


def model_creation(toxic_data, features):
    '''
    Create models and measure cross validation scores and pickle models.
    '''
    target_columns = list(toxic_data.columns)[2:]

    models = {}
    scores = []

    for col in target_columns:
        target = toxic_data[col]
        classifier = LogisticRegression(C=20, class_weight='balanced')

        accuracy = np.mean(cross_val_score(classifier, features, target, cv=3, scoring='roc_auc'))
        scores.append(accuracy)
        print('Accuracy score for {} is {}'.format(col, accuracy))

        classifier.fit(features, target)
        print('Building model for column: {}'.format(col))
        models[col] = classifier

    print('Total accuracy score is {}'.format(np.mean(scores)))

    # save models into pickle files
    for col in target_columns:
        filename = 'toxicity_models/model_{}.sav'.format(col)
        pickle.dump(models[col], open(filename, 'wb'))

if __name__ == '__main__':
    '''
    Trains models on kaggle toxic comment dataset (https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge/data).
    Builds and saves 2 vectorizers and 6 toxicity models.
    '''
    from build_toxicity_models import LemmaTokenizer

    filename = 'kaggle_data/train.csv'
    toxic_data = pd.read_csv(filename)

    # create and pickle vectorizers
    create_vectorizers(toxic_data)

    # create features from vectorizers
    features = feature_creation(toxic_data)

    # train and pickle models
    model_creation(toxic_data, features)