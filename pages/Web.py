import streamlit as st
import s3fs

# streamlit run pages/Web.py
# TODO: Streamlit AWS S3 bucket

"""
# Web Services Test
"""

fs = s3fs.S3FileSystem(anon=False)
output = fs.ls('rosh-bucket-001/media')

output