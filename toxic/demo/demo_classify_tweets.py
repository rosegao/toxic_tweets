# Demo: Classify Tweets
# Rose Gao

import sys
import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from scipy.sparse import hstack


def clean_df(input_filename):
    df = pd.read_csv(input_filename, encoding="ISO-8859-1",
                     usecols=['date', 'fullname', 'id', 'likes', 'replies',
                              'retweets', 'text', 'url', 'user', 'month'])
    # drop NAs
    df = df.dropna()
    # drop duplicates
    df = df.drop_duplicates()
    return df


def classify_tweets(df):
    '''
    Classify tweets and return df
    '''
    # Load vectorizers
    word_vectorizer = pickle.load(open('../toxicity_models/word_vectorizer.pickle', 'rb'))
    char_vectorizer = pickle.load(open('../toxicity_models/char_vectorizer.pickle', 'rb'))

    # Vectorize tweets
    tweet_word_features = word_vectorizer.transform(df['text'])
    tweet_char_features = char_vectorizer.transform(df['text'])
    tweet_features = hstack([tweet_word_features, tweet_char_features])

    # Load models
    loaded_models = {}
    target_columns = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    for col in target_columns:
        loaded_models[col] = pickle.load(open('../toxicity_models/model_{}.sav'.format(col), "rb"))

    # Run models
    for col in target_columns:
        df[col] = loaded_models[col].predict_proba(tweet_features)[:, 1]

    return df

def post_processing_and_export(df, export_filename):
    '''
    Create columns: day, classification, max value
    '''
    df['day'] = [d[:10] for d in df["date"]]
    target_columns = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    df['classification'] = df[target_columns].idxmax(axis=1)
    df['max_value'] = df[target_columns].max(axis=1)

    df.to_csv(export_filename)

if __name__ == '__main__':
    num_args = len(sys.argv)

    if num_args != 2:
        print("usage: python " + sys.argv[0] + " <raw tweets csv>")
        sys.exit(0)

    input_filename = sys.argv[1]
    cleaned_df = clean_df(input_filename)
    classified_df = classify_tweets(cleaned_df)
    export_filename = 'demo_classified_tweets'
    post_processing_and_export(classified_df, export_filename)
    print('Tweets cleaned, classified, and exported! Check folder for classified tweets.')