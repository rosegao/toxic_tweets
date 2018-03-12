# Project: Toxic Tweets
# Filename: classify_tweets.py
# Author: Rose Gao

import sys
import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from scipy.sparse import hstack


def clean_df(input_filename):
    '''
    Read in csv with ISO-8859-1 encoding, drop NAs and duplicates
    Inputs: input_filename: CSV file of raw tweets
    Returns: df: DataFrame of pre-processed tweets
    '''
    df = pd.read_csv(input_filename, encoding="ISO-8859-1",
                     names=['date', 'fullname', 'id', 'likes', 'replies',
                              'retweets', 'text', 'url', 'user', 'month'])
    # drop NAs
    df = df.dropna()
    # drop duplicates
    df = df.drop_duplicates()
    return df


def classify_tweets(df):
    '''
    Load classifiers, classify tweets, and return df
    Inputs: df: DataFrame of tweets
    Returns df: DataFrame of classified tweets
    '''

    # Load vectorizers
    word_vectorizer = pickle.load(open('toxicity_models/word_vectorizer.pickle', 'rb'))
    char_vectorizer = pickle.load(open('toxicity_models/char_vectorizer.pickle', 'rb'))

    # Vectorize tweets
    tweet_word_features = word_vectorizer.transform(df['text'])
    tweet_char_features = char_vectorizer.transform(df['text'])
    tweet_features = hstack([tweet_word_features, tweet_char_features])

    # Load toxicity models
    loaded_models = {}
    target_columns = ['toxic', 'severe_toxic', 'obscene', 'threat',
                      'insult', 'identity_hate']
    for col in target_columns:
        loaded_models[col] = pickle.load(open(
            'toxicity_models/model_{}.sav'.format(col), 'rb'))

    # Run models and fill new target columns
    for col in target_columns:
        df[col] = loaded_models[col].predict_proba(tweet_features)[:, 1]

    return df


def post_processing_and_export(df, export_filename):
    '''
    Create 3 more columns: day, classification, max value
    Inputs:
        df: DataFrame of classified tweets
        export_filename: name of the file to be created
    Returns: no explicit return; creates a CSV from df
    '''
    # Create 'day' column
    df['day'] = [d[:10] for d in df["date"]]

    target_columns = ['toxic', 'severe_toxic', 'obscene', 'threat',
                      'insult', 'identity_hate']

    # Create column using the classification with the highest value for row
    df['classification'] = df[target_columns].idxmax(axis=1)
    # Create column with the highest value for row
    df['max_value'] = df[target_columns].max(axis=1)

    df.to_csv(export_filename)


if __name__ == '__main__':
    num_args = len(sys.argv)

    if num_args != 3:
        print("usage: python " + sys.argv[0] + " <scraped tweets csv>" +
              " <export filename>")
        sys.exit(0)

    input_filename = sys.argv[1]
    cleaned_df = clean_df(input_filename)
    classified_df = classify_tweets(cleaned_df)
    export_filename = sys.argv[2]
    post_processing_and_export(classified_df, export_filename)
    print('Tweets cleaned, classified, and exported!',
          'Check folder for {} csv file.'.format(export_filename))