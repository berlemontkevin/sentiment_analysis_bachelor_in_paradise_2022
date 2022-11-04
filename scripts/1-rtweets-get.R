library("rtweet")
library("dplyr")

vignette("auth")

auth_setup_default()


## store api keys (these are fake example values; replace with your own keys)
api_key <- "7WRzB3IWiSVmJ7Q5uG0lPEPE0"
api_secret_key <- "lPCyQvfWFtq6Z5Ek89ohQCb7nFrbbl76RBHw1mSdIUu2HCHO0U"
access_token <- "934117903791788032-aoGmzlY1NSfJH1WaycL88w3mnDHFwXA"
access_token_secret <- "4PbK1Q7dr29CLSuZBVnW6OfNbdyUa26fZEPo7vYHBN2Ch"
## authenticate via web browser

## authenticate via web browser
token <- create_token(
  app = "BachelorSentimentAnalysis",
  consumer_key = api_key,
  consumer_secret = api_secret_key,
  access_token = access_token,
  access_secret = access_token_secret)

since <- "2022-07-11T00:00:00.000Z"
until <- "2022-07-12T12:00:00.000Z"
news_tweets <- search_tweets("#TheBachelorette", n = 100
                    , include_rts = FALSE
                    , lang = "en"
                    ,'-filter' = "replies", start_time = since, end_time = until, type = "recent")

data_fix <- news_tweets %>%
  # Remove Duplicate
  distinct(text, .keep_all = T) %>%
  # Take The Text Only
  select(created_at, text, favorite_count, mentions_user_id, hashtags, place_full_name)

# Create id column as the tweet identifier
data_fix["id"] <- 1:nrow(data_fix)

# Convert the created_at to date format
data_fix$created_at <- as.Date(data_fix$created_at, format = "%Y-%m-%d")


data_fix


ts_plot(data_fix, "hours")



data_fix %>% 
  filter(!is.na(place_full_name)) %>% 
  count(place_full_name, sort = TRUE) %>% 
  top_n(5)

data_fix %>% 
  arrange(-favorite_count) %>%
  top_n(5, favorite_count) %>% 
  select(created_at, text, favorite_count)


write_as_csv(data_fix, "C:\\Users\\kevin\\OneDrive\\2-code\\bachelorette_sentiment_analysis\\tweets_07_07.csv")



