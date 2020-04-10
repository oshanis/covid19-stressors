import re
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import chart_studio.plotly as py
import plotly.graph_objs as go
import json

def clean_text(text):
    """
    text: input for the text
    Disclaimer:
    This is a ongoing cleaning function
    """

    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "can not ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"he's","he is ",text)
    text = re.sub(r"she's","she is ",text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r"\'scuse", " excuse ", text)
    text = re.sub('\W', ' ', text)
    text = re.sub('\s+', ' ', text)
    text = re.sub(r'[^\w\s]','',text)
    text = text.strip(' ')
    return text

def analyze():
        pd.options.display.max_colwidth = 100
        df = pd.read_csv('compounds.csv',header = None)
        view_stats = df.iloc[0,:]
        print("so we have " + str(view_stats[0]) +" view counts, "+str(view_stats[1])+" likes, "+str(view_stats[2])+" dislikes. ")

        # labels = ['Likecout','Dislikecount']
        # values = [view_stats[1],view_stats[2]]
        # trace = go.Pie(labels=labels, values=values)
        # py.iplot([trace], filename='basic_pie_chart')

        df = df.drop(index = 0)
        df = df.rename(columns = {0:'text',1:'score',2:'likecount'})
        df = df.reset_index(drop = True)
        df['clean_text'] = df['text'].map(lambda com:clean_text(com))
        df.to_csv('clean_comments.csv', sep=',')

        from nltk.sentiment.vader import SentimentIntensityAnalyzer as sid
        sid = sid()
        df['clean_text_score'] = df['clean_text'].map(lambda com:sid.polarity_scores(com)['compound'])
        df.to_csv('sentiment.csv', sep=',')

        df_like_ranking = df.sort_values('likecount',ascending = False)
        df_like_ranking.to_csv('likeranking.csv', sep=',')


if __name__ == "__main__":
    analyze()