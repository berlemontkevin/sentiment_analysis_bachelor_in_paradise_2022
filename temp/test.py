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


#import the src folder as module
# find src folder
# src_path = path.abspath(path.join('..', 'src'))
# sys.path.append(src_path)
sys.path.append(os.path.abspath('..'))
sys.path.append(os.path.abspath('../src'))
import src.data_loading as dl
import src.data_cleaning as dc

# sys.path.append(os.path.abspath('../src'))



# #load the data loading module
# import src.data_loading

start_time = '2022-11-15T18:00:00Z'
# Replace with time period of your choice
end_time = '2022-11-16T18:00:00Z'

#print logging level
temp = dl.getTweets(start_time, end_time)

df = dc.tweetsETL(temp)