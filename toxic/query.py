# query.py  
# Scrape tweets by query term and date range.  Return results in dataframe.
# 
# CS122 Final Project
# Authors: Rose Gao, Andrea Koch, Ian Lyons

from twitterscraper import query_tweets
from datetime import timedelta, date
import pandas as pd
import csv


def write_date(search_date):
	'''
	Takes in a date str of 'MM/DD/YYYY' and formats it for use by datetime
	module.

	Input:
		search_date (str): date in the format 'MM/DD/YYYY'
	Output:
		formatted (object): properly formatted datetime.date object
	'''
	if len(search_date) != 10:
		formatted = print('{}\n{}'.format("INVALID DATE FORMAT",
			                            "Input date str as 'MM/DD/YYYY'"))
	else:
		month = int(search_date[:2])
		day = int(search_date[3:5])
		year = int(search_date[-4:])
		if month > 12:
			formatted = "INVALID MONTH"
			return formatted
		if day > 31:
			formatted = "INVALID DAY"
			return formatted
		if year > 2018:
			formatted = "INVALID YEAR"
			return formatted
		formatted = date(year, month, day)
	return formatted


def twitter_query_over_time(query_term, limit_per_day, starting_date, 
														ending_date):
    '''
	Scrapes tweets and writes them into a dataframe.

	Inputs:
		query_term (str): search term(s) (all in one string)
		limit_per_day (int): max number of tweets to scrape per day 
		starting_date (datetime.date object): start date
		ending_date (datetime.date object): end date
	Output:
		queries_tup (tuple): contains queries (list of results), 
							 start_date (datetime.date object), 
							 end_date (datetime.date object)
    '''
    start_date = write_date(starting_date)
    end_date = write_date(ending_date)
    if start_date > end_date:
        error_statement = "Error:  start date after end date"
        return error_statement
    else:
	    dates = ([start_date + timedelta(days = x) for x 
	    		  in range((end_date - start_date).days + 1)])
	    queries = []    
    	# enumerate through all pairs of dates until the 
    	# second last day/last day pair:
	    for i, date in enumerate(dates[:-1]):
	        query = query_tweets(query = query_term, limit = limit_per_day, 
	                             begindate = dates[i], enddate = dates[i+1], 
	                             poolsize=20, lang='en')
	        queries.extend(query)
	    queries_tup = (queries, start_date, end_date)
	    return queries_tup


def extract_tweets(queries_tup):
	'''
	Extracts pertinent twitter data from query results.

	Input:
		queries_tup (tuple): contains queries (list of results), 
						 start_date (datetime.date object), 
						 end_date (datetime.date object)	
	Output:
		tweets_tup (tuple): contains tweets (list of tweet information), 
							tart_date (datetime.date object), 
							end_date (datetime.date object)		
	'''
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
	'''
	Converts list of tweet information into dataframe.

	Input:
		tweets_tup (tuple): contains tweets (list of tweet information), 
							tart_date (datetime.date object), 
							end_date (datetime.date object)	
	Output:
		df (dataframe): dataframe of tweets with tweet info
	'''
    tweets, start_date, end_date = tweets_tup
    df = pd.DataFrame(tweets) 
    df['month'] = df['date'].apply(lambda x : date(x.year, x.month, 1))
    df = df.dropna()
    df = df.drop_duplicates()
    # check and drop values outside of queried range once more
    # (b/c twitter_scraper is wonky):
    df = df[df['date'] >= start_date]
    df = df[df['date'] <= end_date]
    return df


def go(query_term, limit_per_day, starting_date, ending_date, filename):
	'''
	Scrapes for tweets, converts to dataframe, and writes to CSV file.

	Inputs:
		query_term (str): search term(s) (all in one string)
		limit_per_day (int): max number of tweets to scrape per day 
		starting_date (str): date in the format 'MM/DD/YYYY'
		ending_date (str): date in the format 'MM/DD/YYYY'
		filename (str): csv filename of your choice
	Output:
		generates a CSV file titled by the filename parameter
	'''
	queries_tup = twitter_query_over_time(query_term, limit_per_day, 
									  starting_date, ending_date)
	tweets_tup = extract_tweets(queries_tup)
	df = format_tweets_as_df(tweets_tup)
	df.to_csv(filename, mode='a', header=False)







