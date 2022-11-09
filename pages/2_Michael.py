import streamlit as st

import pandas as pd

import plotly.express as px


from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt

st.title('Michael Sentiment Analysis')

dates = [ '09_27','10_04','10_11','10_17','10_18', '10_24', '10_25', '10_31']


candidates = ['michael']


df_sentiments = pd.DataFrame(columns=['Candidate','Neg Tweets','Number Tweets','Date'])
df_numbers = pd.DataFrame(columns=candidates, index=dates)

for date in dates:
    temp_df = pd.read_csv(f'./data_web_app/{date}.csv')
    for candidate in candidates:
        nbr_positive = 0
        nbr_negative = 0
        nbr_neutral = 0
        count = 0
        for i in range(len(temp_df['sentiment'])):
            if temp_df['text'][i].lower().find(candidate) != -1:
                if temp_df['sentiment'][i] == 'Negative':
                    nbr_negative += 1
                elif temp_df['sentiment'][i] == 'Positive':
                    nbr_positive += 1
                else:
                    nbr_neutral += 1
                count += 1

        # only add if there are enough tweets about the candidate
        if count > 100:
            df_sentiments = df_sentiments.append({'Candidate':candidate,'Neg Tweets':nbr_negative/count,'Number Tweets':count,'Date':date}, ignore_index=True)
        # add a row to df_sentiments
        # df_sentiments = df_sentiments.append({'Candidate':candidate,'Neg Tweets':nbr_negative/(count),'Number Tweets':count,'Date':date}, ignore_index=True)

        # st.dataframe(df_sentiments)
        # df_sentiments.append(pd.DataFrame({'Candidate':candidate,'Neg Tweets':nbr_negative /( nbr_negative + nbr_positive + nbr_neutral),'Number Tweets':count,'Date':date}))
        # df_sentiments['Neg Tweets'][date] = nbr_negative /( nbr_negative + nbr_positive + nbr_neutral)
        # df_sentiments['Candidate'][date] = candidate
        # df_sentiments['Number Tweets'][date] = count


st.markdown('Let us first look at the evolution of the sentiment of the tweets about Michael through the show:')


fig_men = px.line(df_sentiments, x='Date', y='Neg Tweets', markers = True, color = 'Candidate', title = 'Proportion of negative tweets about men contestants', labels = {'index':'Date', 'value':'Proportion of negative tweets', 'variable':'Candidate'})
st.plotly_chart(fig_men)



st.markdown('### Let us now look at the most frequent words used in the tweets about Michael:')

option = st.selectbox(
     'Which type of keywords would you like to look at?',
     ('Positive', 'Negative', 'Neutral'))
# Wordcloud with positive tweets
for date in dates:
    temp_df = pd.read_csv(f'./data_web_app/{date}.csv')
    # get the tweets where sentiment is the option and candidate is in it
    positive_tweets = temp_df['text'][temp_df[(temp_df['sentiment'] == option) & (temp_df['text'].str.lower().str.contains('michael'))]]
    # positive_tweets = temp_df['text'][temp_df["sentiment"] == option && temp_df['text'][i].lower().find(candidate) != -1]
    stop_words = ["https", "co", "RT"] + list(STOPWORDS)
    positive_wordcloud = WordCloud(max_font_size=50, max_words=50, background_color="white", stopwords = stop_words).generate(str(positive_tweets))

    st.write(f'Wordcloud for {option} tweets on {date}')
    fig, ax = plt.subplots(figsize=(10, 10))
    # ax.title("Positive Tweets - Wordcloud")
    ax.imshow(positive_wordcloud, interpolation="bilinear")
    # ax.axis("off")
    st.pyplot(fig)

    #save the most frequent word
    df_numbers[candidate][date] = positive_wordcloud.words_.most_common(1)[0][0]

st.markdown('### Let us now look at the most frequent words used in the tweets about Michael:')
st.dataframe(df_numbers)

    