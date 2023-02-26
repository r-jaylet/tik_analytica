import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from fetch_trends import fetch_top_trends, hashtag_trend_info, music_trend_info
from fetch_data import fetch_top_influencers, user, user_videos, hashtag, music
from format import human_format


def display_trends_data():

    df_hashtag, df_music, df_creator, df_tiktok = fetch_top_trends()

    st.header('Trending hashtags', anchor=None)
    st.dataframe(df_hashtag)
    st.header('Trending musics', anchor=None)
    st.dataframe(df_music)
    st.header('Trending creators', anchor=None)
    st.dataframe(df_creator)
    st.header('Trending tiktoks', anchor=None)
    st.dataframe(df_tiktok)


def display_influ_data(country):
    df_influ = fetch_top_influencers(country)
    st.dataframe(df_influ, height=3000)

    st.download_button(
        label="Download data as CSV",
        data=df_influ,
        file_name=f'df_{country}.csv',
    )


def display_user_data(username_):
    json_user = user(username_)
    df_user_info = pd.DataFrame.from_dict(json_user, orient='index')
    df_user = user_videos(username_)
    df_user_videos = pd.DataFrame.from_records(df_user)
    df_view = df_user_videos.copy()
    df_user_videos['createdAt'] = pd.to_datetime(df_user_videos['createdAt'])

    st.header('Profile description', anchor=None)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(df_user_info[0].avatar, width=300, caption=df_user_info[0].nickname)
    with col2:
        st.text_area(
            'User info',
            f'unique id: {df_user_info[0].uniqueId}\n\n'
            f'id: {df_user_info[0].id}\n\n'
            f'bio link: {df_user_info[0].bioLink}\n\n'
            f'private account: {df_user_info[0].privateAccount}',
            height=300,
            label_visibility='collapsed')
    with col3:
        before = df_user_videos[df_user_videos['createdAt'] <= datetime.now() - timedelta(days=7)]
        ratio_vid = len(df_user_videos) / int((datetime.now() - df_user_videos.iloc[-1].createdAt).days / 7)
        before_ratio_vid = len(before) / int((datetime.now() - before.iloc[-1].createdAt).days / 7)
        delt = (ratio_vid - before_ratio_vid) / ratio_vid
        st.metric('Videos / week', human_format(ratio_vid), delta=human_format(delt * 100) + '%', delta_color="normal")

        ratio_views = df_user_videos['playCount'].sum() / len(df_user_videos)
        before = df_user_videos.iloc[1:]
        delt = (ratio_views - (before['playCount'].sum() / len(before))) / ratio_views
        st.metric('Average views / video', human_format(ratio_views), delta=human_format(delt * 100) + '%',
                  delta_color="normal")

        engagement = df_user_videos['likesCount'].sum() / df_user_videos['playCount'].sum()
        before_engagement = df_user_videos.iloc[1:]['likesCount'].sum() / df_user_videos.iloc[1:]['playCount'].sum()
        delt = (engagement - before_engagement) / engagement
        st.metric('Engagement rate', human_format(engagement), delta=human_format(delt * 100) + '%',
                  delta_color="normal")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_area('fol', f'followers : {df_user_info[0].followers}', height=25, label_visibility='collapsed')
    with col2:
        st.text_area('foll', f'following : {df_user_info[0].following}', height=25, label_visibility='collapsed')
    with col3:
        st.text_area('like', f'like count : {df_user_info[0].hearts}', height=25, label_visibility='collapsed')
    with col4:
        st.text_area('vid', f'vid count : {df_user_info[0].videos}', height=25, label_visibility='collapsed')

    st.header('TikTok list', anchor=None)
    st.dataframe(df_view[['id', 'description', 'createdAt', 'duration',
                          'shareCount', 'likesCount', 'commentCount', 'playCount',
                          'downloadURL', 'directVideoUrl']], height=200)

    st.header('Main metrics', anchor=None)
    df_user_videos = df_user_videos.sort_values('createdAt')
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Views per video', anchor=None)
        st.area_chart(list(df_user_videos['playCount']))
    with col2:
        st.subheader('Engagement rate per video', anchor=None)
        st.area_chart(df_user_videos['shareCount'] * df_user_videos['likesCount'] / df_user_videos['playCount'])

    words = df_user_videos.description.str.split(expand=True).stack().value_counts().keys()
    st.header('Main hashtags used', anchor=None)
    hasht = [i for i in words if i.startswith('#')][:4]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_area('h0', f'{hasht[0]}', height=25, label_visibility='collapsed')
    with col2:
        st.text_area('h1', f'{hasht[1]}', height=25, label_visibility='collapsed')
    with col3:
        st.text_area('h2', f'{hasht[2]}', height=25, label_visibility='collapsed')
    with col4:
        st.text_area('h3', f'{hasht[3]}', height=25, label_visibility='collapsed')

    st.header('Main collaborators', anchor=None)
    collab = [i for i in words if i.startswith('@')][:5]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_area('c0', f'{collab[0]}', height=25, label_visibility='collapsed')
    with col2:
        st.text_area('c1', f'{collab[1]}', height=25, label_visibility='collapsed')
    with col3:
        st.text_area('c2', f'{collab[2]}', height=25, label_visibility='collapsed')
    with col4:
        st.text_area('c3', f'{collab[3]}', height=25, label_visibility='collapsed')

    st.download_button(
        label="Download data as CSV",
        data=df_user_videos.to_csv().encode('utf-8'),
        file_name=f'df_{username_}.csv',
    )


def display_hashtag_data(tag_):

    country = 'France'
    period = '120'

    stats, trend, region_info, related_hashtags = hashtag_trend_info(tag_, country, period)

    st.header('Post stats', anchor=None)
    col1, col2 = st.columns(2)
    with col1:
        st.text_area(
            'Posts',
            f'Last {period} days, {country}\n\n : {stats[0]}'
            f'Overall Views : {stats[1]}',
            height=100)
    with col2:
        st.text_area(
            'Posts',
            f'Last {period} days, {country}\n\n : {stats[2]}'
            f'Overall Views : {stats[3]}',
            height=100)

    st.header('Trend analysis', anchor=None)
    st.write(trend)

    st.header('Region info', anchor=None)
    st.dataframe(region_info)

    st.header('Related hashtag', anchor=None)
    st.dataframe(related_hashtags)

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
        st.text_area('a0', f'@{authors[0]}', height=25, label_visibility='collapsed')
    with col2:
        st.text_area('a1', f'@{authors[1]}', height=25, label_visibility='collapsed')
    with col3:
        st.text_area('a2', f'@{authors[2]}', height=25, label_visibility='collapsed')
    with col4:
        st.text_area('a3', f'@{authors[3]}', height=25, label_visibility='collapsed')

    st.header('Associated hashtags', anchor=None)
    words = df_hash.description.str.split(expand=True).stack().value_counts().keys()
    hasht = [i for i in words if i.startswith('#')][:4]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.text_area('h0', f'{hasht[0]}', height=25, label_visibility='collapsed')
    with col2:
        st.text_area('h1', f'{hasht[1]}', height=25, label_visibility='collapsed')
    with col3:
        st.text_area('h2', f'{hasht[2]}', height=25, label_visibility='collapsed')
    with col4:
        st.text_area('h3', f'{hasht[3]}', height=25, label_visibility='collapsed')

    st.download_button(
        label="Download data as CSV",
        data=df_hash.to_csv().encode('utf-8'),
        file_name=f'df_{tag_}.csv',
    )


def display_music_data(music_):

    df_music = music(music_)
    df_music = pd.DataFrame.from_dict(df_music, orient='index')

    music_tag = f'{df_music[0].title}-{df_music[0].id}'
    country = 'France'
    period = '120'

    trend, region_info, music_info = music_trend_info(music_tag, country, period)

    st.header('Trend analysis', anchor=None)
    st.write(trend)

    st.header('Region info', anchor=None)
    st.dataframe(region_info)

    st.header('Related hashtag', anchor=None)
    st.dataframe(music_info)

    st.header('Music info', anchor=None)
    col1, col2 = st.columns(2)
    with col1:
        st.image(df_music[0].coverLarge, width=300, caption=df_music[0].title)
    with col2:
        st.text_area(
            'Music info',
            f'title: {df_music[0].title}\n\n'
            f'id: {df_music[0].id}\n\n'
            f'author: {df_music[0].author}\n\n'
            f'original: {df_music[0].original}\n\n'
            f'album: {df_music[0].album}\n\n'
            f'duration: {df_music[0].duration}',
            height=300,
            label_visibility='collapsed')

    st.download_button(
        label="Download data as CSV",
        data=df_music.to_csv().encode('utf-8'),
        file_name=f'df_{music_}.csv',
    )


# Set the page title
st.set_page_config(page_title='Data Search', page_icon=':bar_chart:', layout='wide')

# Add the three buttons
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Top trends', 'Top influencers',
                                        'User search', 'Hashtag search', 'Music search'])

with tab1:
    st.title('Top trends')
    st.caption('Most important trends from the past 7 days around the world !')
    display_trends_data()

with tab2:
    st.title('Top influencers')
    influ_type = st.text_input(
        'Search for country',
        placeholder=' example : fr, us...',
        help='Type in country code')
    if st.button('Search influencers'):
        display_influ_data(influ_type)


with tab3:
    st.title('User Data')
    user_type = st.text_input(
        'Search for user',
        placeholder=' example : taylorswift, therock...',
        help='Type in username of TikToker')
    if st.button('Search user'):
        display_user_data(user_type)

with tab4:
    st.title('Hashtag Data')
    tag_type = st.text_input(
        'Search for hashtag',
        placeholder=' example : jazz, rap...',
        help='Type in hashtag of a specific challenge')
    if st.button('Search hashtag'):
        display_hashtag_data(tag_type)

with tab5:
    st.title('Music Data')
    music_type = st.text_input(
        'Search for music',
        placeholder=' example : https://www.tiktok.com/@ayanakamura/video/7190099178314386693...',
        help='Type in url of a TikTok')
    if st.button('Search music'):
        display_music_data(music_type)
