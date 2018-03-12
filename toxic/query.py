# query.py  
# Run query and return results in dataframe.
# 
# CS122 Final Project
# Rose Gao, Andrea Koch, Ian Lyons

from twitterscraper import query_tweets
from datetime import timedelta, date
import pandas as pd
import csv
#import itertools


def write_date(search_date):
	if len(search_date) != 10:
		formatted = print('{}\n{}'.format("invalid date format",
			                            "input date str as MM/DD/YYYY"))
	else:
		month = int(search_date[:2])
		day = int(search_date[3:5])
		year = int(search_date[-4:])
		if month > 12:
			formatted = "invalid month"
			return formatted
		if day > 31:
			formatted = "invalid day"
			return formatted
		if year > 2018:
			formatted = "invalid year"
			return formatted
		formatted = date(year, month, day)
	return formatted


def twitter_query_over_time(query_term, limit_per_day, starting_date, ending_date):
    # create dates between start_date and end_date
    start_date = write_date(starting_date)
    end_date = write_date(ending_date)
    if start_date > end_date:
        error_statement = "Error:  start date after end date"
        return error_statement
    else:
	    dates = [start_date + timedelta(days = x) for x in range((end_date - start_date).days + 1)]
	    queries = []    
    	# enumerate through all pairs of dates until the second last day/last day pair
	    for i, date in enumerate(dates[:-1]):
	        query = query_tweets(query = query_term, limit = limit_per_day, 
	                             begindate = dates[i], enddate = dates[i+1], 
	                             poolsize=20, lang='en')
	        queries.extend(query)
	    queries_tup = (queries, start_date, end_date)
	    return queries_tup


def extract_tweets(queries_tup):
    queries, start_date, end_date = queries_tup
    tweets = []
    for tweet in queries:
        tweets.append({'date': tweet.timestamp, 'text': tweet.text, 
                       'fullname': tweet.fullname, 'id': tweet.id, 
                       'likes': tweet.likes, 'replies': tweet.replies,
                       'retweets': tweet.retweets, 'url': tweet.url,
                       'user': tweet.user})
    tweets_tup = (tweets, start_date, end_date)
    return tweets_tup


def format_tweets_as_df(tweets_tup):
    tweets, start_date, end_date = tweets_tup
    df = pd.DataFrame(tweets) 
    df['month'] = df['date'].apply(lambda x : date(x.year, x.month, 1))
    df = df.dropna()
    df = df.drop_duplicates()
    # check and drop values outside of queried range (b/c twitter_scraper is wonky)
    df = df[df['date'] >= start_date]
    df = df[df['date'] <= end_date]
    return df


def write_to_csv(output_path_filename, df):
    df.to_csv(output_path_filename, mode='a', header=False)

    # with open(output_filename, 'w') as csv_file:
    # 	writer = csv.writer(csv_file, delimiter=',')
    # 	for index, row in df.iterrows():
    # 		writer.writerow([index, row])

def go(query_term, limit_per_day, starting_date, ending_date, output_path_filename):
	queries_tup = twitter_query_over_time(query_term, limit_per_day, 
									  starting_date, ending_date)
	tweets_tup = extract_tweets(queries_tup)
	df = format_tweets_as_df(tweets_tup)
	write_to_csv(output_path_filename, df)







