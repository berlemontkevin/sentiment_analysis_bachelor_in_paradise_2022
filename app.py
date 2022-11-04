import streamlit as st

import pandas as pd

import plotly.express as px

st.title('Homepage of the Sentiment Analysis of Bachelor In Paradise 2022')

dates = [ '09_27','10_04','10_11','10_17','10_18', '10_24', '10_25', '10_31']

candidates = ['brandon', 'michael','romeo','shanae','jill','johnny','brittany','justin','hunter','sierra','hailey','kira','lace']

df_sentiments = pd.DataFrame(columns=['Candidate','Neg Tweets','Number Tweets','Date'])
df_numbers = pd.DataFrame(columns=candidates, index=dates)
# dd a dummy row to df_sentiments

df_sentiments = df_sentiments.append({'Candidate':'dummy','Neg Tweets':0,'Number Tweets':0,'Date':'dummy'}, ignore_index=True)

for date in dates:
    temp_df = pd.read_csv(f'./data/{date}.csv')
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

        # add a row to df_sentiments
        df_sentiments = df_sentiments.append({'Candidate':candidate,'Neg Tweets':nbr_negative/(count),'Number Tweets':count,'Date':date}, ignore_index=True)

        # st.dataframe(df_sentiments)
        # df_sentiments.append(pd.DataFrame({'Candidate':candidate,'Neg Tweets':nbr_negative /( nbr_negative + nbr_positive + nbr_neutral),'Number Tweets':count,'Date':date}))
        # df_sentiments['Neg Tweets'][date] = nbr_negative /( nbr_negative + nbr_positive + nbr_neutral)
        # df_sentiments['Candidate'][date] = candidate
        # df_sentiments['Number Tweets'][date] = count

# list all the women from candidates

women = ['shanae','jill','brittany','hunter','sierra','hailey','kira','lace']
men = ['brandon','michael','romeo','johnny','justin']

df_women = df_sentiments[df_sentiments.Candidate.isin(women)]
df_men = df_sentiments[df_sentiments.Candidate.isin(men)]

# rachel_contestants = ['rachel', 'tino', 'aven', 'zach']
# rachel_df = df_sentiments[rachel_contestants]
# gabby_contestants = ['gabby', 'erich', 'johnny', 'jason']
# # gabby_df = df_sentiments[gabby_contestants]
# st.dataframe(df_sentiments)
# st.dataframe(df_men)

st.markdown('Let us first look at the evolution of the sentiment of the tweets about men contestants thruogh the show:')
fig_men = px.line(df_men, x='Date', y='Neg Tweets', markers = True, color = 'Candidate', title = 'Proportion of negative tweets about men contestants', labels = {'index':'Date', 'value':'Proportion of negative tweets', 'variable':'Candidate'})
st.plotly_chart(fig_men)

st.markdown('Let us first look at the evolution of the sentiment of the tweets about women contestants thruogh the show:')
fig_women = px.line(df_women, x='Date', y='Neg Tweets', markers = True, color = 'Candidate', title = 'Proportion of negative tweets about women contestants', labels = {'index':'Date', 'value':'Proportion of negative tweets', 'variable':'Candidate'})
st.plotly_chart(fig_women)


# Let's plot the last day as histogram

hist_men = px.box(df_men, x=men, y="Neg Tweets", title ="Proportion of Negative tweets about a contestant")
st.plotly_chart(hist_men)

#same thing for women
hist_women = px.box(df_women, x=women, y="Neg Tweets")
st.plotly_chart(hist_women)


# st.markdown('Now we look at the evolution of the sentiment of the tweets about gabby\'s contestants thruogh the show:')
# fig_gabby = px.line(gabby_df, x=gabby_df.index, y=gabby_df.columns, markers = True, title = 'Proportion of negative tweets about gabby\'s contestants', labels = {'index':'Date', 'value':'Proportion of negative tweets', 'variable':'Candidate'})
# st.plotly_chart(fig_gabby)
