import pandas as pd


def get_tweets(query, df_name):
    from twitterscraper import query_tweets
    '''
    Calls the query_tweets function and returns 
    the value as a dataframe while storing it in a csv file
    input: the query (string) | the dataframe/file-name (string)
    output: return of the query in a csv file | and a dataframe
    '''
    tweets = query_tweets(query)
    df = pd.DataFrame(t.__dict__ for t in tweets)
    df.to_csv(f'{df_name}.csv')

def cleanup_columns(df, to_drop, names):
    '''
    Drops unnecessary columns and renames the final ones
    input: df (dataframe ) | to_drop (list) | names (list)
    output: a dataframe with useful columns and columns name 
    '''
    df = df.drop(to_drop, axis=1)
    df.columns = names
    return df

def cleanup_rows(df):
    '''
    Drops all the duplicates and rows with a nan
    input: df (dataframe)
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
        index=['All', 'All Unique', 'En Unique', 'Not En Unique', 'Duplicate']
        )

def display_img(url):
    '''
    returns an HTML image tag
    input: url (string)
    output: HTML tag with src of given url
    '''
    return f'<img src="{url}" width=150 height=150>'

def top_characteristics(_top_tweets, tops):
    result = pd.DataFrame(
        columns=[
            'hasMedia', 
            'hasHashtag',
            'avarage hashtags',
            'avarage text length', 
            'avarage likes',
            'avarage retweet',
            'avarage replies',
            'avarage isReplied'
            ], 
        index=[
            f'{tops} Tweets'
            ]
        )
    
    result['hasMedia'] = len(_top_tweets[_top_tweets['hasMedia'] == True])
    result['hasHashtag'] = len(_top_tweets[_top_tweets['hashtags'].str.len() != 0])
    result['avarage hashtags'] = sum(_top_tweets['hashtags'].str.len()) / tops
    result['avarage text length'] = sum(_top_tweets['text'].str.len()) / tops
    result['avarage likes'] = sum(_top_tweets['likes']) / tops
    result['avarage retweet'] = sum(_top_tweets['retweets']) / tops
    result['avarage replies'] = sum(_top_tweets['replies']) / tops
    result['avarage isReplied'] = sum(_top_tweets['isReplied']) / tops
    return result
