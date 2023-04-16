from collections import defaultdict
import s3fs
from tools.utils import read_toml


def get_file_endings(paths):
    file_endings = defaultdict(int)
    [file_endings.update({file.split('.')[-1]: file_endings[file.split('.')[-1]] + 1}) for file in paths]
    # Sort the dictionary by value in descending order
    sorted_file_endings = {k: v for k, v in sorted(file_endings.items(), key=lambda item: item[1], reverse=True)}
    print(sorted_file_endings)


toml = read_toml()
bucket = toml['AWS_STORAGE_BUCKET_NAME']

fs = s3fs.S3FileSystem(anon=False)
filenames = fs.find(bucket)

print(f'Found {len(filenames):,} files in bucket.')
get_file_endings(filenames)
