import streamlit as st
import pandas as pd

from fetch_data import user, user_videos, hashtag, music


def display_user_data(username_):
    json_user = user(username_)
    df_user_info = pd.DataFrame.from_dict(json_user, orient='index')

    st.header('Profile info', anchor=None)
    col1, col2 = st.columns(2)
    with col1:
        st.image(df_user_info[0].avatar, width=300, caption=df_user_info[0].nickname)
    with col2:
        st.text(f'unique id: {df_user_info[0].uniqueId}')
        st.text(f'id: {df_user_info[0].id}')
        st.text(f'secret uid: {df_user_info[0].secretUID}')
        st.text(f'bio link: {df_user_info[0].bioLink}')
        st.text(f'private account: {df_user_info[0].privateAccount}')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text(f'followers : {df_user_info[0].followers}')
    with col2:
        st.text(f'following : {df_user_info[0].following}')
    with col3:
        st.text(f'like count : {df_user_info[0].hearts}')
    with col4:
        st.text(f'vid count : {df_user_info[0].videos}')

    st.header('TikTok list', anchor=None)
    df_user = user_videos(username_)
    df_user_videos = pd.DataFrame.from_records(df_user)
    st.dataframe(df_user_videos[['id', 'description', 'createdAt', 'duration',
                                 'shareCount', 'likesCount', 'commentCount', 'playCount',
                                 'downloadURL', 'directVideoUrl']], height=200)

    st.header('Main metrics', anchor=None)
    col1, col2 = st.columns(2)
    df_user_videos['createdAt'] = pd.to_datetime(df_user_videos['createdAt'])
    df_user_videos = df_user_videos.sort_values('createdAt')
    with col1:
        st.subheader('Views per video', anchor=None)
        st.area_chart(list(df_user_videos['playCount']))
    with col2:
        st.subheader('Engagement rate per video', anchor=None)
        st.area_chart(list(df_user_videos['shareCount'] * df_user_videos['likesCount'] * df_user_videos['commentCount']) / df_user_videos['playCount'])

    words = df_user_videos.description.str.split(expand=True).stack().value_counts().keys()
    st.header('Main hashtags used', anchor=None)
    hasht = [i for i in words if i.startswith('#')][:4]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text(f'{hasht[0]}')
    with col2:
        st.text(f'{hasht[1]}')
    with col3:
        st.text(f'{hasht[2]}')
    with col4:
        st.text(f'{hasht[3]}')

    st.header('Main collaborators', anchor=None)
    collab = [i for i in words if i.startswith('@')][:5]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text(f'{collab[0]}')
    with col2:
        st.text(f'{collab[1]}')
    with col3:
        st.text(f'{collab[2]}')
    with col4:
        st.text(f'{collab[3]}')


def display_hashtag_data(tag_):

    st.header('TikTok list', anchor=None)
    df_hash = hashtag(tag_)
    df_hash = pd.DataFrame.from_records(df_hash)
    st.dataframe(df_hash[['id', 'description', 'createdAt', 'duration',
                                 'shareCount', 'likesCount', 'commentCount', 'playCount',
                                 'downloadURL']], height=200)

    st.header('Associated TikTokers', anchor=None)
    authors = list(df_hash.author)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text(f'@{authors[0]}')
    with col2:
        st.text(f'@{authors[1]}')
    with col3:
        st.text(f'@{authors[2]}')
    with col4:
        st.text(f'@{authors[3]}')

    st.header('Associated hashtags', anchor=None)
    words = df_hash.description.str.split(expand=True).stack().value_counts().keys()
    hasht = [i for i in words if i.startswith('#')][:4]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text(f'{hasht[0]}')
    with col2:
        st.text(f'{hasht[1]}')
    with col3:
        st.text(f'{hasht[2]}')
    with col4:
        st.text(f'{hasht[3]}')


def display_music_data(music_):
    df_music = music(music_)
    df_music = pd.DataFrame.from_dict(df_music, orient='index')

    st.header('Music info', anchor=None)
    col1, col2 = st.columns(2)
    with col1:
        st.image(df_music[0].coverLarge, width=300, caption=df_music[0].title)
    with col2:
        st.text(f'title: {df_music[0].title}')
        st.text(f'id: {df_music[0].id}')
        st.text(f'author: {df_music[0].author}')
        st.text(f'duration: {df_music[0].duration}')
        st.text(f'original: {df_music[0].original}')
        st.text(f'album: {df_music[0].album}')


# Set the page title
st.set_page_config(page_title='Data Search', page_icon=':bar_chart:', layout='wide')

# Add the three buttons
tab1, tab2, tab3 = st.tabs(['User', 'Hashtag', 'Music'])

with tab1:
    st.title('User Data')
    user_type = st.text_input(
        'Search for user',
        placeholder=' example : taylorswift, therock...',
        help='Type in username of TikToker'
    )
    if st.button('Search user'):
        display_user_data(user_type)

with tab2:
    st.title('Hashtag Data')
    tag_type = st.text_input(
        'Search for hashtag',
        placeholder=' example : jazz, rap...',
        help='Type in hashtag of a specific challenge'
    )
    if st.button('Search hastag'):
        display_hashtag_data(tag_type)

with tab3:
    st.title('Music Data')
    music_type = st.text_input(
        'Search for music',
        placeholder=' example : https://www.tiktok.com/@ayanakamura/video/7190099178314386693...',
        help='Type in url of a TikTok'
    )
    if st.button('Search music'):
        display_music_data(music_type)
