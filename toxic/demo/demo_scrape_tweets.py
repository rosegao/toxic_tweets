# Project: Toxic Tweets
# Filename: demo_scrape_tweets.py
# Author: Rose Gao

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

    if num_args != 4:
        print("usage: python " + sys.argv[0] + " <query>" + " <start date>"
              + " < end date>")
        sys.exit(0)

    query = sys.argv[1]
    limit_per_day = 10
    sd = sys.argv[2].split('-')
    sd_ints = list(map(int, sd))
    start_date = date(sd_ints[0], sd_ints[1], sd_ints[2])
    ed = sys.argv[3].split('-')
    ed_ints = list(map(int, ed))
    end_date = date(ed_ints[0], ed_ints[1], ed_ints[2])

    tweets = twitter_query(query, limit_per_day, start_date, end_date)
    print('Finished query!')

    df = format_tweets_as_df(tweets, start_date, end_date)
    df.to_csv('demo_scraped_tweets')
    print('Check folder for scraped tweets.')