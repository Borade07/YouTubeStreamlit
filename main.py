import streamlit as st
from pytube import *
from pytube.exceptions import *
import os

st.set_page_config(
    page_title="YouTube Downloader",
    page_icon='yt.png',
)
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.title("YouTube VIDEO/AUDIO DOWNLOADER..")
name = st.text_input("Enter Your YouTube URL Here")

if st.checkbox("Playlist"):
    st.text("Check Only If you have enter the Playlist URL")

if (st.button('Check URL')):
    try:
        yt = YouTube(name)
        result = yt.title
        st.success(result)
    except:
        try:
            pl = Playlist(name)
            result = pl.title
            st.success(result)
        except:
            st.error("Something went wrong with url")

status = st.radio("Select Video Quality: ", ('1080', '720', '480', '360', '144'))
videoq = [0]
videoqn = ['1080']
if status == '1080':
    videoq[0] = 137
    videoqn[0] = '1080'
elif status == '720':
    videoq[0] = 22
    videoqn[0] = '720'
elif status == '360':
    videoq[0] = 18
    videoqn[0] = '360'
elif status == '480':
    videoq[0] = 135
    videoqn[0] = '480'
elif status == '144':
    videoq[0] = 17
    videoqn[0] = '144'
else:
    st.error("plz Select the quality of video")

if (st.button('Download Video')):
    try:
        yt = YouTube(name)
        yt.streams.filter(progressive=True)
        yt.streams.filter(adaptive=True)
        stream = yt.streams.get_by_itag(videoq[0])
        st.info(f'Downloading Video of Quality {videoqn[0]}p')
        stream.download()
        st.success(f'{yt.title} download successfully')

    except:
        try:
            pl = Playlist(name)
            st.info(f'There are Total {pl.length} Videos in Playlist with {videoqn[0]}p')
            n = 1
            for video in pl.videos:
                try:
                    video.streams.filter(progressive=True)
                    video.streams.filter(adaptive=True)
                    st.info(f'Video Name : {video.title}')
                    n = n + 1
                except VideoUnavailable:
                    st.warning(f'Video {video.title} is unavaialable, skipping... ')
                except RegexMatchError:
                    print('The Regex pattern did not return any matches for the video: {}'.format(video))

                except ExtractError:
                    print('An extraction error occurred for the video: {}'.format(video))

                else:
                    video.streams.get_by_itag(videoq[0]).download()
                    st.success(f'{video.title} download successfully')
        except:
            st.error("something went wrong when you are downloading video")

if (st.button('Download audio')):
    try:
        yt = YouTube(name)
        # yt.streams.filter(progressive=True)
        # yt.streams.filter(adaptive=True)
        # stream = yt.streams.filter(only_audio=True)
        stream = yt.streams.filter(only_audio=True).first()
        st.info('Downloading Audio')
        # download the file
        out_file = stream.download()

        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        st.success(" audio download successfully")
    except:
        try:
            pl = Playlist(name)
            n = 1
            st.success(f'There are Total {pl.length} Videos in Playlist')
            for video in pl.videos:
                try:
                    video.streams.filter(progressive=True)
                    video.streams.filter(adaptive=True)
                    st.info(f'Music Name : {video.title}')
                    n = n + 1
                except VideoUnavailable:
                    st.warning(f'Music {video.title} is unavailable, skipping... ')
                else:
                    stream = video.streams.filter(only_audio=True).first()
                    out_file = stream.download()
                    base, ext = os.path.splitext(out_file)
                    new_file = base + '.mp3'
                    os.rename(out_file, new_file)
                    st.success(f'{video.title} download successfully')
        except:
            st.error("something went wrong when you are downloading audio")


# Markdown
st.markdown("""
	Copyright &copy; 2021 Amey Borade
""",unsafe_allow_html=True)
