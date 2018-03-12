# File title:  Query2.py  
# Run query and return results in dataframe.  Our methods employ 
# TwitterScraper (the scraping tool provided by Twitter), given a search topic (str), maximum 
# number of tweets to scrape daily, and a start and end date

# 
# CS122 Final Project
# Author: Andrea Koch

from twitterscraper import query_tweets
from datetime import timedelta, date
import pandas as pd
import csv



def write_date(starting_date, ending_date):
	'''
	Takes in a start and end date and returns a tuple which 
	'''
	leap_years = [2008, 2012, 2016]
	thirty_days = [4, 6, 9, 11]
	thirty_one_days = [1, 3, 5, 7, 8, 10, 12] 
	if (len(starting_date) != 10) or (len(ending_date) != 10):
		check_statement = print('{}\n{}'.format("INVALID DATE INPUT",
			                            "Input date str as 'MM/DD/YYYY'"))
		return check_statement
	else:
		start_month = int(starting_date[:2])
		start_day = int(starting_date[3:5])
		start_year = int(starting_date[-4:])
		end_month = int(ending_date[:2])
		end_day = int(ending_date[3:5])
		end_year = int(ending_date[-4:])
		first_start_day = start_day - 1
		first_start_month = start_month
		first_start_year = start_year
		second_start_day = start_day
		second_start_month = start_month
		second_start_year = start_year
		new_end_day = end_day + 1
		new_end_month = end_month
		new_end_year = end_year

		#input check
		if ((start_year > 2018) or (start_year < 2006)
		or (end_year > 2018) or (end_year < 2006)):
			check_statement = "INVALID YEAR: Query range is 2006-2018"
			return check_statement
		if start_year > end_year:
			check_statement = "START DATE AFTER END DATE"
			return check_statement

		#checks for beginning and end of month
		if start_day == 1:
			# months with 31 days but not January, March or August
			if start_month in thirty_one_days:
				if start_month not in [1, 3, 8]:
					first_start_day = 30
					first_start_month = start_month - 1
					first_start_year = start_year
				elif start_month == 1:
					first_start_day = 31
					first_start_month = 12
					first_start_year = start_year - 1
				elif (start_month == 3):
					if start_year in leap_years:
						first_start_day = 29
						first_start_month = 2
						first_start_year = start_year
					else:
						first_start_day = 28
						first_start_month = 2
						first_start_year = start_year
				elif (start_month == 8):
					first_start_day = 31
					first_start_month = 7
					first_start_year = start_year
			elif start_month in thirty_days:
				first_start_day = 31
				first_start_month = start_month - 1
				first_start_year = start_year
			elif start_month == 2:
				first_start_day = 31
				first_start_month = 1
				first_start_year = start_year

		if end_month == 2: 
			if (end_day == 29) and (end_year in leap_years):
				new_end_month = 3
				new_end_day = 1
				new_end_year = end_year 
			elif (end_day == 28) and (end_year not in leap_years):
				new_end_month = 3
				new_end_day = 1
				new_end_year = end_year

		if (end_month == 12) and (end_day == 31):
			new_end_month = 1
			new_end_day = 1
			new_end_year = end_year + 1
		if ((end_month != 12) and (end_day == 31) 
		and (end_month in thirty_one_days)):
				new_end_month = end_month + 1
				new_end_day = 1
				new_end_year = end_year
		if ((end_month != 12) and (end_day == 30) 
		and (end_month in thirty_days)):
			new_end_month = end_month + 1
			new_end_day = 1
			new_end_year = end_year

	start_date = date(start_year, start_month, start_day)
	end_date = date(end_year, end_month, end_day)
	first_start_date = date(first_start_year, first_start_month, first_start_day)
	second_start_date = date(second_start_year, second_start_month, second_start_day)
	new_end_date = date(new_end_year, new_end_month, new_end_day)
	date_tup = (start_date, 
				end_date, 
				first_start_date, 
				second_start_date, 
				new_end_date)

	return date_tup


def query_to_df(query_term, limit_per_day, start_date, end_date):
    # create dates between start_date and end_date
    queries = query_tweets(query = query_term, limit = limit_per_day, 
                         begindate = start_date, enddate = end_date, 
                         poolsize=20, lang='en')
    tweets = []
    for tweet in queries:
    	tweets.append({'date': tweet.timestamp, 'text': tweet.text, 
                       'fullname': tweet.fullname, 'id': tweet.id, 
                       'likes': tweet.likes, 'replies': tweet.replies,
                       'retweets': tweet.retweets, 'url': tweet.url,
                       'user': tweet.user})
    df = pd.DataFrame(tweets) 
    df['month'] = df['date'].apply(lambda x : date(x.year, x.month, 1))
    df = df.dropna()
    df = df.drop_duplicates()
    return df


def clean_and_merge(df1, df2, start_date, end_date):
	# check and drop values outside of queried range (b/c twitter_scraper is wonky)
	df1 = df1[df1['date'] >= start_date]
	df1 = df1[df1['date'] <= end_date]
	df2 = df2[df2['date'] >= start_date]
	df2 = df2[df2['date'] <= end_date]
	df = pd.concat([df1, df2])
	df = df.dropna()
	df = df.drop_duplicates()
	return df


def go(query_term, limit_per_day, starting_date, ending_date, filename):
	date_tup = write_date(starting_date, ending_date)
	start_date, end_date = date_tup[0:2]
	first_start_date, second_start_date, new_end_date = date_tup[2:]
	df1 = query_to_df(query_term, limit_per_day, 
									  first_start_date, new_end_date)
	df2 = query_to_df(query_term, limit_per_day,
									  second_start_date, new_end_date)
	df = clean_and_merge(df1, df2, start_date, end_date)
	df.to_csv(path_or_buf=filename, header=None)





