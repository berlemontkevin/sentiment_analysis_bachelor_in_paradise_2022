# Script that downloads the data from the web and stores it in the data folder

# Path: scripts/getting_data.py

#define the project as sys path
import sys
import os
# sys.path.append(os.path.abspath('..'))

#import logging
import logging.config
from os import path
log_file_path = path.join('../logging.ini')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


#Define the start_dates and end_dates
start_dates = ['2022-09-06T18:00:00Z','2022-09-07T18:00:00Z','2022-09-13T18:00:00Z','2022-09-27T18:00:00Z','2022-10-04T18:00:00Z','2022-10-10T18:00:00Z','2022-10-11T18:00:00Z','2022-10-17T18:00:00Z','2022-10-18T18:00:00Z','2022-10-24T18:00:00Z','2022-10-25T18:00:00Z','2022-10-31T18:00:00Z','2022-11-14T18:00:00Z','2022-11-15T18:00:00Z']

end_dates = ['2022-09-07T18:00:00Z', '2022-09-08T18:00:00Z','2022-09-14T18:00:00Z','2022-09-28T18:00:00Z','2022-10-05T18:00:00Z','2022-10-11T18:00:00Z','2022-10-12T18:00:00Z','2022-10-18T18:00:00Z','2022-10-19T18:00:00Z','2022-10-25T18:00:00Z','2022-10-26T18:00:00Z','2022-11-01T18:00:00Z','2022-11-15T18:00:00Z','2022-11-16T18:00:00Z']

# #import the src folder as module
# # find src folder
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../src'))
import src.data_loading as dl
import src.data_cleaning as dc

# #create the name of all the files
# for i in range(len(start_dates)):
#     keyword = "#BachelorInParadise"
#     start_time = start_dates[i]
#     end_time = end_dates[i]
#     file_name = f'{keyword}_{start_time}_{end_time}.csv'
#     logger.info(file_name)

# download and save the data

dl.save_raw_data_multiple_dates(start_dates, end_dates, num_tweet=40000)
dl.save_sentiment_analysis_multiple_dates(start_dates, end_dates)