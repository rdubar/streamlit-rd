#!/usr/bin/python
from tools.media_record import MediaRecord
import os, random, time
from tools.utils import showtime

MEDIA_LIST = '/Users/roger/PycharmProjects/streamlit-rd/data/media.txt'

def get_library_records(path=MEDIA_LIST, verbose=True):
    clock = time.perf_counter()
    if not os.path.exists(path):
        print(f'Movie List Path not found: {path}')
        return []
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    records = []
    for entry in lines:
        parts = entry.split()
        if len(parts) < 3:
            continue
        if parts[-1].lower() == 'extras':
            extras = True
            parts = parts[:-1]
        else:
            extras = False
        quality = parts[-1]
        source = parts[-2]
        year = parts[-3]
        if year and len(year)==6 and year[0]=='(' and year[5]==')' and year[1:5].isdigit():
            year = year[1:5]
            title = ' '.join(parts[:-3])
        else:
            title = ' '.join(parts[:-2])
            year = None
        m = MediaRecord(title=title, year=year, source=source, quality=quality, extras=extras)
        records.append(m)
    if len(records) == 0:
        print(f'No media records found in {path}')
    clock = time.perf_counter() - clock
    if verbose: print(f'Found {len(records):,} records from the media list in {showtime(clock)}.')
    return records

def main():
    records = get_library_records()
    n = len(records)
    r = random.randint(0,n)
    item = records[r]
    print(f'Item {r:,} of {n:,} is: {item}')

if __name__== "__main__" :
    main()