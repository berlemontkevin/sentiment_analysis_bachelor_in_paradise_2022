# FIle with the functions necessary for data cleaning

#Initialize logging
import logging
from os import path
# log_file_path = path.join('../logging.ini')
# logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)


#Import modules
import pandas as pd
import re


from transformers import pipeline


def cleanTweets(tweet:list) -> str:
    '''
    This function will clean the tweets by removing the links, hashtags, mentions and special characters
    Args:
        text (str): The text to be cleaned
    Returns:
        clean_text (str): The cleaned text
    '''
    logger.debug('Cleaning the tweet')
    try:
        text = tweet.text
        clean_text = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",text).split())
    except Exception as e:

        logger.debug(type(tweet.text))
        logger.debug(tweet)
        logger.error('Error cleaning the tweets', exc_info=True)
        

    return clean_text



def tweetsETL(tweets:list) -> pd.DataFrame:

    '''
    This function will extract the relevant information from the tweets and transform it into a dataframe
    Args:
        tweets (list): The list of tweets
    Returns:
        tweets_df (pd.DataFrame): The dataframe containing the relevant information from the tweets
        '''    
    result = []
    #function to unpack the tweets list into a dataframe
    logger.info('Extracting the relevant information from the tweets')
    for tweet in tweets:
           
            try:
                
                clean_text = cleanTweets(tweet)
                result.append({'id': tweet.id,
                           'text': tweet.text,
                           'clean_tweet' : clean_text,
                           'created_at': tweet.created_at,
                           'source':tweet.source,
                           'retweets': tweet.public_metrics['retweet_count'],
                           'replies': tweet.public_metrics['reply_count'],
                           'likes': tweet.public_metrics['like_count'],
                           'quote_count': tweet.public_metrics['quote_count']
                      })
            except:
                #Debug print the tweet.text
              
                logger.error('Error unpacking the tweets', exc_info=True)

    #add a log info
    logger.info('Tweets unpacked')
    df = pd.DataFrame(result)
    return df


def sentimentAnalysis(df:pd.DataFrame) -> pd.DataFrame:
    '''
    This function will perform sentiment analysis on the tweets and add the results to the dataframe
    Args:
        df (pd.DataFrame): The dataframe containing the tweets
    Returns:
        df (pd.DataFrame): The dataframe containing the tweets and the sentiment analysis
    '''
    #add a log info
    logger.info('Performing sentiment analysis')
    try:
        #initialize the sentiment analysis pipeline
        specific_model = pipeline(model="cardiffnlp/twitter-roberta-base-sentiment-latest")
        specific_model.save_pretrained("./twitter_roberta")
        #perform the sentiment analysis
        df['sentiment'] = df['clean_tweet'].apply(lambda x: specific_model(x)[0]['label'])
        df['score'] = df['clean_tweet'].apply(lambda x: specific_model(x)[0]['score'])
    except:
        logger.error('Error performing sentiment analysis', exc_info=True)
    #add a log info
    logger.info('Sentiment analysis performed')
    return df


