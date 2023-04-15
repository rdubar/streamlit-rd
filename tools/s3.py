import s3fs

fs = s3fs.S3FileSystem(anon=False)
filenames = fs.find('rosh-bucket-001')


print(f'Found {len(filenames):,} files in bucket.')

from collections import defaultdict
# Dictionary comprehension to count file endings
file_endings = defaultdict(int)
[file_endings.update({file.split('.')[-1]: file_endings[file.split('.')[-1]] + 1}) for file in filenames]

# Sort the dictionary by value in descending order
sorted_file_endings = {k: v for k, v in sorted(file_endings.items(), key=lambda item: item[1], reverse=True)}

print(sorted_file_endings)