import os
import pandas
import numpy as np

from settings import DATAFRAME_FILE
from tools.utils import show_file_size

def get_quality(x):
    if type(x) == int:
        x = int(x)
        if x > 1500:
            x = '4K'
        elif x >= 800:
            x = 'HD'
        elif x > 400:
            x = 'SD'
        else:
            x = 'ZD'
    if not x or x == None or x == '':
        return 'UQ'
    return x.upper()

def get_dataframe(data, path=DATAFRAME_FILE):
    df = pandas.DataFrame([vars(s) for s in data])
    #df = df.sort_values(by=['added'])
    df = df[['title', 'year', 'quality', 'source','added','search']].astype(np.int64, errors='ignore')
    df['added'] = pandas.to_datetime(df["added"]).dt.date
    df['quality'] = df['quality'].apply(get_quality)
    df.set_index('title', inplace=True)
    df = df.fillna('')
    try:
        df.to_pickle(path)
    except Exception as e:
        warn(f'get_dataframe: Failed to save to {path}: {e}')
        return None
    s = os.path.getsize(path)
    print(f'Saved dataframe to: {path} ({show_file_size(s)}).')
    df['added'] = pandas.to_datetime(df['added'])
    df_sorted = df.sort_values(by=['added'], na_position='last', ascending=False)
    return df_sorted