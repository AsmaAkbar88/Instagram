import streamlit as st
import requests
import re
import uuid

# Streamlit UI
st.title("Instagram Video Downloader ⏳")
url = st.text_input("Enter Instagram Video URL: ")

# Function to sanitize the URL and make it a valid file name
def sanitize_filename(url):
    # Remove unwanted characters and make the file name valid
    return re.sub(r'[^\w\s-]', '', url.split('/')[-1]) + f"_{uuid.uuid4().hex}.mp4"

# Function to download video
def download_video(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = sanitize_filename(url)
            with open(filename, "wb") as f:
                f.write(response.content)
            return f"Download Successful! Video saved as {filename}"
        else:
            return "Failed to Download"
    except Exception as e:
        return f"Error: {e}"

if st.button("Download") and url:
    message = download_video(url)
    if "Successful" in message:
        st.success(message)
    else:
        st.error(message)
else:
    st.error("Please enter a valid URL.")
