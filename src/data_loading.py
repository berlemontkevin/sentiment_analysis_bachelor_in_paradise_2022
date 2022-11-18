# This file will define all the necessary data loading functions for the project

#adding project path
import sys
sys.path.append('/home/kberlemo/projects/sentiment_bachelor_analysis_in_paradise_2022')

#Initialize logging from the logging.ini file in the project directory
import logging
logger = logging.getLogger(__name__)


#Importing the necessary packages
import configparser
import tweepy
import pandas as pd

#import the config file from config.py 
import os
sys.path.append(os.path.abspath('..'))
try:
    import config
except:
    logger.error('Error importing the config file', exc_info=True)


import data_cleaning as dc

def getTweets(start_time:str, stop_time:str, num_tweet = 10, keyword = '#BachelorInParadise') -> list:
    '''
    This function will get the tweets from the twitter API and return them as a list
    Args:
        start_time (str): The start time of the tweets to be collected
        stop_time (str): The stop time of the tweets to be collected
        num_tweet (int): The number of tweets to be collected
        keyword (str): The keyword to be searched for
    Returns:
        tweets (str): The dataframe containing the tweets

    '''
    #Get the twitter API credentials from the config file    
    #asking for the search term and the desired number of tweets
   
    query = f'{keyword} -is:retweet lang:en'
    num_tweets = int(num_tweet)
    #connecting to the twitter API using clent and the bearer_token credentials from config.ini

    try:

        btk = config.bearer_key
        client = tweepy.Client(bearer_token=btk)

    except Exception as e:
        logger.error('Error connecting to the twitter API', exc_info=True)
    
    
    #using tweepy paginator to get over 100 last tweets from twitter api
    tweets = []
    for tweet in tweepy.Paginator(client.search_recent_tweets,
                                    query = query,                            
                                    tweet_fields = ['id','created_at', 'public_metrics', 'text', 'source'],
                                    start_time = start_time, end_time = stop_time,
                                    max_results = 100).flatten(limit=num_tweets):
    
        tweets.append(tweet)

    # add as log INFO the number of tweets collected
    logger.info(f'Number of tweets collected: {len(tweets)}')
    return tweets


# Function that get the data, clean it and save it to a csv file
def save_raw_data(start_time:str, stop_time:str, num_tweet = 10, keyword = '#BachelorInParadise') -> None:
    '''
    This function will get the tweets from the twitter API, clean them and save them to a csv file
    Args:
        start_time (str): The start time of the tweets to be collected
        stop_time (str): The stop time of the tweets to be collected
        num_tweet (int): The number of tweets to be collected
        keyword (str): The keyword to be searched for
    Returns:
        None
    '''
    #get the tweets
    tweets = getTweets(start_time, stop_time, num_tweet, keyword)
    #clean the tweets
    tweets_df = dc.tweetsETL(tweets)
    #save the tweets to a csv file
    tweets_df.to_csv(f'../data/raw/{keyword}_{start_time}_{stop_time}.csv', index = False)
    logger.info(f'Saved the raw data to ../data/raw/{keyword}_{start_time}_{stop_time}.csv')


def save_sentiment_analysis(start_time:str, stop_time:str, num_tweet = 10, keyword = '#BachelorInParadise') -> None:
    '''
    This function will gread the csv of tweets and perform sentiment analysis and save them to a csv file
    Args:
        start_time (str): The start time of the tweets to be collected
        stop_time (str): The stop time of the tweets to be collected
        num_tweet (int): The number of tweets to be collected
        keyword (str): The keyword to be searched for
    Returns:
        None
    '''
    #read the csv file
    tweets_df = pd.read_csv(f'../data/raw/{keyword}_{start_time}_{stop_time}.csv')
    #perform sentiment analysis
    tweets_df = dc.sentimentAnalysis(tweets_df)
    #save the tweets to a csv file
    tweets_df.to_csv(f'../data/processed/{keyword}_{start_time}_{stop_time}.csv', index = False)
    logger.info(f'Saved the processed data to ../data/processed/{keyword}_{start_time}_{stop_time}.csv')

# Function that take a list of dates and save the raw data for all of them
def save_raw_data_multiple_dates(dates_start:list, dates_end:list, num_tweet = 10, keyword = '#BachelorInParadise') -> None:
    '''
    This function will get the tweets from the twitter API, clean them and save them to a csv file
    Args:
        dates_start (list): The list of start times of the tweets to be collected
        dates_end (list): The list of stop times of the tweets to be collected
        num_tweet (int): The number of tweets to be collected
        keyword (str): The keyword to be searched for
    Returns:
        None
    '''
    #loop over the dates and save the raw data
    for i in range(len(dates_start)):
        # if the file exist, do nothing
        if os.path.exists(f'../data/raw/{keyword}_{dates_start[i]}_{dates_end[i]}.csv'):
            logger.info(f'File ../data/raw/{keyword}_{dates_start[i]}_{dates_end[i]}.csv already exist')
        else:    
            save_raw_data(dates_start[i], dates_end[i], num_tweet, keyword)


#Function that take a list of dates and save the processed data for all of them
def save_sentiment_analysis_multiple_dates(dates_start:list, dates_end:list, num_tweet = 10, keyword = '#BachelorInParadise') -> None:
    '''
    This function will gread the csv of tweets and perform sentiment analysis and save them to a csv file
    Args:
        dates_start (list): The list of start times of the tweets to be collected
        dates_end (list): The list of stop times of the tweets to be collected
        num_tweet (int): The number of tweets to be collected
        keyword (str): The keyword to be searched for
    Returns:
        None
    '''
    #loop over the dates and save the processed data
    for i in range(len(dates_start)):
        # if the file exist, do nothing
        if os.path.exists(f'../data/processed/{keyword}_{dates_start[i]}_{dates_end[i]}.csv'):
            logger.info(f'File ../data/processed/{keyword}_{dates_start[i]}_{dates_end[i]}.csv already exist')
        else:
            save_sentiment_analysis(dates_start[i], dates_end[i], num_tweet, keyword)




#create the name = main function to test the function
if __name__ == '__main__':
    # import logging.config
    # logging.config.fileConfig('../logging.ini',disable_existing_loggers=False)

    start_time = '2022-11-15T18:00:00Z'
    # Replace with time period of your choice
    end_time = '2022-11-16T18:00:00Z'
    temp = getTweets(start_time, end_time)
    # logger.info(type(temp))
    # logger.info(type(temp[0].text))