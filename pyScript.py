#!/usr/bin/python3

import pandas as pd

def get_tweets(query, df_name):
    from twitterscraper.query import query_tweets_once
    '''
    Calls the query_tweets_once function and stors it in a csv file
    :params: the query (string) | the dataframe/file-name (string)
    :return: 
    '''
    tweets = query_tweets_once(query, pos=1)
    df = pd.DataFrame(t.__dict__ for t in tweets)
    df.to_csv(f'{df_name}.csv')

def html_scrap(url, parser_type='html.parser'):
    from bs4 import BeautifulSoup
    import requests
    '''
    Scrap the given url 
    :params: the url (string)
    :return: html content (HTML)
    '''
    page = requests.get(url)
    html = BeautifulSoup(page.content, parser_type)
    html.findAll(class_='css-1dbjc4n')
    return html


def cleanup_columns(df, to_drop, names):
    '''
    Drops unnecessary columns and renames the final ones
    :params: df (dataframe ) | to_drop (list) | names (list)
    :return: a dataframe with useful columns and columns name 
    '''
    df = df.drop(to_drop, axis=1)
    df.columns = names
    return df

def cleanup_rows(df):
    '''
    Drops all the duplicates and rows with a nan
    :params: df (dataframe)
    outpu: df (dataframe)
    '''
    df = df.drop_duplicates(['tweetId'], keep='first')
    df = df.dropna(subset=['text'], axis=0)
    return df

def row_analysing(df, all_tweets):
    from langdetect import detect
    '''
    THIS IS NO LONGER USED
    '''
    non_eng_tweets = sum([1 for t in df['text'] if df(t) == 'en'])
    unique_tweets = df.shape[0]
    unique_tweets_en = df.shape[0] - non_eng_tweets
    duplicate_tweets = all_tweets - df.shape[0]
    return pd.DataFrame(
        {'tweets':[all_tweets, unique_tweets, unique_tweets_en, non_eng_tweets, duplicate_tweets]}, 
        index=['All', 'All Unique', 'En Unique', 'Not En Unique', 'Duplicate'])

def display_img(url):
    '''
    returns an HTML image tag
    :params: url (string)
    :return: HTML tag with src of given url
    '''
    return f'<img src="{url}" width=150 height=150>'

def top_characteristics(_top_tweets, tops):
    '''
    Will analyse the given tweets and return it as a pandas DataFrame
    :params: _top_tweets (dataFrame) | tops (int) => nr of tops
    :return: dataFrame
    '''
    result = pd.DataFrame(index=[f'{tops} Tweets'])
    
    result['hasMedia'] = len(_top_tweets[_top_tweets['hasMedia'] == True])
    result['hasHashtag'] = sum([1 for i in _top_tweets['hashtags'] if len(i)>2])
    result['avarage text length'] = sum(_top_tweets['text'].str.len()) / tops
    result['avarage likes'] = sum(_top_tweets['likes']) / tops
    result['avarage retweet'] = sum(_top_tweets['retweets']) / tops
    result['avarage replies'] = sum(_top_tweets['replies']) / tops
    result['avarage isReplyTo'] = sum(_top_tweets['isReplyTo']) / tops
    return result

def create_wordcloud(data, mask=None, title=None, stop_words=''):
    import nltk
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    '''
    Creates and shows a word-cloud
    '''
    stopwords = nltk.corpus.stopwords.words('english')
    _stop_words = stop_words
    stopwords.extend(_stop_words)
    
    wordcloud = WordCloud(
        background_color='black',
        mask=mask,
        stopwords=stopwords,
        max_words=50,
        max_font_size=500, 
        scale=3,
        random_state=2
    ).generate(str(data))

    fig = plt.figure(1, figsize=(15, 20))
    plt.axis('off')
    if title: 
        fig.suptitle(title, fontsize=20)
        fig.subplots_adjust(top=2.3)

    plt.imshow(wordcloud)
    plt.show()
    