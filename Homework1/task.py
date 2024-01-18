import chardet
import numpy as np
import pandas as pd


def task1():
    datas = []
    for i in range(1, 5):
        path = './data/combined_data_{}.txt'.format(i)
        data = pd.read_csv(path, sep=',', skiprows=1)
        datas.append(data.values)
    all_data = np.vstack(datas)
    all_data = pd.DataFrame(all_data)
    all_data.columns = ['CustomerID', 'Rating', 'Date']
    all_data['Date'] = pd.to_datetime(all_data['Date'])
    rating_count = len(all_data['Rating'])
    distinct_user = all_data['CustomerID'].nunique()
    start_year = all_data['Date'].min()
    end_year = all_data['Date'].max()
    return rating_count, distinct_user, start_year, end_year


def split_data(x):
    x = str(x).split(',')
    movie_id = x[0]
    YearOfRelease = x[1]
    Title = ''.join(x[2:])
    return pd.Series([movie_id, YearOfRelease, Title])


def task2():
    with open('./data/movie_titles.csv', 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']
    data = pd.read_csv('./data/movie_titles.csv', encoding=encoding, error_bad_lines=False, header=None, sep='`')
    data.columns = ['temp']
    data[['movie_id', 'YearOfRelease', 'Title']] = data['temp'].apply(split_data)
    data.drop(['temp'], inplace=True, axis=1)
    distinct_movie = data['movie_id'].nunique()
    refer_four_data = data.groupby('Title').filter(lambda x: x['movie_id'].nunique() >= 4)
    refer_four = refer_four_data['Title'].nunique()
    return distinct_movie, refer_four


def task3():
    datas = []
    for i in range(1, 5):
        path = './data/combined_data_{}.txt'.format(i)
        data = pd.read_csv(path, sep=',', skiprows=1)
        movie_id = pd.read_csv(path, sep=',', nrows=0)
        movie_id = movie_id.columns[0].replace(':', '')
        data['movie_id'] = movie_id
        datas.append(data.values)
    all_data = np.vstack(datas)
    all_data = pd.DataFrame(all_data)
    all_data.columns = ['CustomerID', 'Rating', 'Date', 'movie_id']
    all_data['Date'] = pd.to_datetime(all_data['Date'])
    # filter
    exactly_user = all_data.groupby('CustomerID').filter(lambda x: x['Rating'].sum() == 200)
    print(len(exactly_user['CustomerID']))
    min_id = exactly_user['CustomerID'].min()
    like_movie = exactly_user[(exactly_user['CustomerID'] == min_id) & (exactly_user['Rating'] >= 5)]
    like_movie_id = like_movie['movie_id'].values
    # read movie data
    with open('./data/movie_titles.csv', 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']
    movie_data = pd.read_csv('./data/movie_titles.csv', encoding=encoding, error_bad_lines=False, header=None, sep='`')
    movie_data.columns = ['temp']
    movie_data[['movie_id', 'YearOfRelease', 'Title']] = movie_data['temp'].apply(split_data)
    movie_data.drop(['temp'], inplace=True, axis=1)
    movie_name = movie_data[movie_data['movie_id'].isin(like_movie_id)]['Title']
    return exactly_user.nunique(), movie_name.values

print(task3())