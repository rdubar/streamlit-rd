import streamlit as st
import s3fs

"""
# Web Services Test
"""

bucket = st.secrets['AWS_STORAGE_BUCKET_NAME']
fs = s3fs.S3FileSystem(anon=False)
filenames = fs.find(bucket)

maximum = 30
count = 0
output = ''
for item in filenames:
    ending = item.split('.')[-1]
    if ending or 'thumb' in item:
        lower = ending.lower()
    if not ending or lower not in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp']:
        continue
    # st.image(fs.url(item), width=100)
    output += f'<img src="{fs.url(item)}" width=100>'
    count += 1
    if count > maximum:
        break
st.markdown(output, unsafe_allow_html=True)
