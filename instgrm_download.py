import streamlit as st
import instaloader
import re
import uuid
import os
import shutil

st.title("📥 Instagram Video Downloader")

url = st.text_input("Paste Instagram Post/Reel URL:")

def sanitize_filename(url):
    return re.sub(r'[^\w\s-]', '', url.split('/')[-2]) + f"_{uuid.uuid4().hex}.mp4"

def download_video_only(url):
    try:
        temp_folder = "temp_video"
        os.makedirs(temp_folder, exist_ok=True)

        L = instaloader.Instaloader(dirname_pattern=temp_folder, download_video_thumbnails=False,
                                    download_geotags=False, download_comments=False, save_metadata=False)

        shortcode = url.split("/")[-2]
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        L.download_post(post, target="video_temp")

        for file in os.listdir(temp_folder):
            if file.endswith(".mp4"):
                new_name = sanitize_filename(url)
                shutil.move(os.path.join(temp_folder, file), new_name)
                shutil.rmtree(temp_folder)
                return "✅ Download Successful!"
        
        shutil.rmtree(temp_folder)
        return "❌ Video not found."

    except Exception as e:
        return f"❌ Error: {e}"

if st.button("Download") and url:
    message = download_video_only(url)
    if "✅" in message:
        st.success(message)
    else:
        st.error(message)

