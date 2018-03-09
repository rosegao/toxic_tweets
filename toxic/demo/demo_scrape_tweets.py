# Demo: Scrape Tweets
# Rose Gao

import sys
from twitterscraper import query_tweets
from datetime import timedelta, date
import pandas as pd
import csv


def twitter_query(query, limit_per_day, start_date, end_date):
    '''
    Extract query
    '''
    tweets = []
    query = query_tweets(query = query, limit = limit_per_day,
                             begindate = start_date, enddate = end_date,
                             poolsize=20, lang='en')
    for tweet in query:
        tweets.append({'date': tweet.timestamp, 'text': tweet.text,
                       'fullname': tweet.fullname, 'id': tweet.id,
                       'likes': tweet.likes, 'replies': tweet.replies,
                       'retweets': tweet.retweets, 'url': tweet.url,
                       'user': tweet.user})
    return tweets

def format_tweets_as_df(tweets, start_date, end_date):
    '''
    Clean df
    '''
    df = pd.DataFrame(tweets)

    # add timestamp column
    df['month'] = df['date'].apply(lambda x: date(x.year, x.month, 1))

    # drop NAs
    df = df.dropna()

    # drop duplicates
    df = df.drop_duplicates()

    # drop values outside of queried range
    df = df[df['date'] >= start_date]
    df = df[df['date'] <= end_date]
    return df


if __name__ == '__main__':
    num_args = len(sys.argv)

    if num_args != 2:
        print("usage: python " + sys.argv[0] + " <query>")
        sys.exit(0)

    query = sys.argv[1]
    limit_per_day = 10
    start_date = date(2018, 2, 24)
    end_date = date(2018, 3, 9)

    tweets = twitter_query(query, limit_per_day, start_date, end_date)
    print('Finished query!')

    df = format_tweets_as_df(tweets, start_date, end_date)
    df.to_csv('demo_scraped_tweets')
    print('Check folder for scraped tweets.')