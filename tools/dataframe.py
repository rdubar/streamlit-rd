import os
import pandas as pd
import numpy as np

from settings import DATAFRAME_PATH
from tools.utils import show_file_size, sort_by_attrib_value, warn


def get_quality(x, group=True):
    """ Return quality based on video height """
    if group:
        if type(x) == str and x.isdigit():
            x = int(x)
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
        x = str(x).upper()
        if not x in ['4K', 'HD', 'SD', 'ZD', 'UQ']:
            x = 'UQ'
        return x
    else:
        n = 0
        if type(x) == str:
            lower = x.lower()
            if '4k' in lower:
                n = 2160
            elif 'hd' in lower:
                n = 1080
        if not n and x.isdigit():
            n = int(x)
        return n


def get_dataframe(data, path=DATAFRAME_PATH):
    """ Convert list of media objects into pandas dataframe and save to file """
    # Sort data to ensure the newest added titles appear first
    data = sort_by_attrib_value(data, 'added', reverse=True)
    df = pd.DataFrame([vars(s) for s in data])
    df = df[['title', 'year', 'quality', 'source', 'added', 'search']].astype(np.int64, errors='ignore')
    df['added'] = pd.to_datetime(df["added"]).dt.date
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
    df['added'] = pd.to_datetime(df['added'])
    df_sorted = df.sort_values(by=['added'], na_position='last', ascending=False)
    return df_sorted


def main():
    pass


if __name__ == "__main__":
    main()
