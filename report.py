import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from fetch_trends import fetch_top_trends, hashtag_trend_info, music_trend_info, fetch_top_influencers
from fetch_data import user, user_videos, hashtag, music
from format import human_format


def display_trends_data():
    df_hashtag, df_music, df_creator, df_tiktok = fetch_top_trends()

    st.header('Trending hashtags', anchor=None)
    st.dataframe(df_hashtag, width=1350)

    st.header('Trending musics', anchor=None)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(df_music.iloc[0].cover, caption=df_music.iloc[0].music, width=200)
        st.write('title : ', df_music.iloc[0].music)
        st.write('author : ', df_music.iloc[0].author)
        st.write('link : ', df_music.iloc[0].link)
    with col2:
        st.image(df_music.iloc[1].cover, caption=df_music.iloc[1].music, width=200)
        st.write('title : ', df_music.iloc[1].music)
        st.write('author : ', df_music.iloc[1].author)
        st.write('link : ', df_music.iloc[1].link)
    with col3:
        st.image(df_music.iloc[2].cover, caption=df_music.iloc[2].music, width=200)
        st.write('title : ', df_music.iloc[2].music)
        st.write('author : ', df_music.iloc[2].author)
        st.write('link : ', df_music.iloc[2].link)
    with col4:
        st.image(df_music.iloc[3].cover, caption=df_music.iloc[3].music, width=200)
        st.write('title : ', df_music.iloc[3].music)
        st.write('author : ', df_music.iloc[3].author)
        st.write('link : ', df_music.iloc[3].link)
    with col5:
        st.image(df_music.iloc[4].cover, caption=df_music.iloc[4].music, width=200)
        st.write('title : ', df_music.iloc[4].music)
        st.write('author : ', df_music.iloc[4].author)
        st.write('link : ', df_music.iloc[4].link)

    st.header('Trending creators', anchor=None)
    st.dataframe(df_creator, width=1350)
    st.header('Trending tiktoks', anchor=None)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(df_tiktok.iloc[0].cover, width=200)
        st.write('id : ', df_tiktok.iloc[0].id)
        st.write('title : ', df_tiktok.iloc[0].title)
        st.write('link : ', df_tiktok.iloc[0].itemUrl)

    with col2:
        st.image(df_tiktok.iloc[1].cover, width=200)
        st.write('id : ', df_tiktok.iloc[1].id)
        st.write('title : ', df_tiktok.iloc[1].title)
        st.write('link : ', df_tiktok.iloc[1].itemUrl)
    with col3:
        st.image(df_tiktok.iloc[2].cover, width=200)
        st.write('id : ', df_tiktok.iloc[2].id)
        st.write('title : ', df_tiktok.iloc[2].title)
        st.write('link : ', df_tiktok.iloc[2].itemUrl)
    with col4:
        st.image(df_tiktok.iloc[3].cover, width=200)
        st.write('id : ', df_tiktok.iloc[3].id)
        st.write('title : ', df_tiktok.iloc[3].title)
        st.write('link : ', df_tiktok.iloc[3].itemUrl)

    with col5:
        st.image(df_tiktok.iloc[4].cover, width=200)
        st.write('id : ', df_tiktok.iloc[4].id)
        st.write('title : ', df_tiktok.iloc[4].title)
        st.write('link : ', df_tiktok.iloc[4].itemUrl)


def display_influ_data(country):
    df_influ = fetch_top_influencers(country)
    st.header(f'Top 5 influencers in {country}', anchor=None)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(df_influ.iloc[0].profilePicUrl, caption=df_influ.iloc[0].fullName, width=200)
    with col2:
        st.image(df_influ.iloc[1].profilePicUrl, caption=df_influ.iloc[1].fullName, width=200)
    with col3:
        st.image(df_influ.iloc[2].profilePicUrl, caption=df_influ.iloc[2].fullName, width=200)
    with col4:
        st.image(df_influ.iloc[3].profilePicUrl, caption=df_influ.iloc[3].fullName, width=200)
    with col5:
        st.image(df_influ.iloc[4].profilePicUrl, caption=df_influ.iloc[4].fullName, width=200)
    st.header('Full ranking', anchor=None)
    st.dataframe(df_influ.drop('profilePicUrl', axis=1), height=3000, width=1350)

    st.download_button(
        label='Download data as CSV',
        data=df_influ.to_csv(index=False).encode("utf-8"),
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
    country = 'FR'
    period = '30'
    stats, trend, region_info, related_hashtags = hashtag_trend_info(tag_, country, period)

    st.header(f'Post stats in {country}', anchor=None)
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"Number of post in last {period} days", value=stats[0])
        st.metric(label="Number of posts overall", value=stats[1])

    with col2:
        st.metric(label=f"Number of views in last {period} days", value=stats[2])
        st.metric(label="Number of views overall", value=stats[3])

    st.header('Trend analysis', anchor=None)
    st.write(trend)

    st.header('Region info', anchor=None)
    st.dataframe(region_info)

    st.header('Related hashtags', anchor=None)
    st.dataframe(related_hashtags.T)

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
    country = 'FR'
    period = '120'
    trend, region_info, music_info = music_trend_info(music_tag, country, period)

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

    st.header('Trend analysis', anchor=None)
    st.write(trend)

    st.header('Region info', anchor=None)
    st.dataframe(region_info)

    st.header('Related songs', anchor=None)
    st.dataframe(music_info)

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
    # Top trends page
    st.title('Top trends')
    st.caption('Most important trends from the past 7 days around the world !')
    display_trends_data()

with tab2:
    # Top influencers page
    st.title('Top influencers')
    option = st.selectbox(
        'Search for the following country?',
        ('USA', 'France', 'UK', 'Germany', 'Italy', 'Spain', 'Portugal'))
    code_count = {'USA': 'us',
                  'France': 'fr',
                  'UK': 'uk',
                  'Germany': 'de',
                  'Italy': 'it',
                  'Spain': 'es',
                  'Portugal': 'pt'}
    display_influ_data(code_count[option])

with tab3:
    # User search page
    st.title('User Data')
    user_type = st.text_input(
        'Search for user',
        placeholder=' example : taylorswift, therock...',
        help='Type in username of TikToker')
    if st.button('Search user'):
        display_user_data(user_type)

with tab4:
    # Hashtag search page
    st.title('Hashtag Data')
    tag_type = st.text_input(
        'Search for hashtag',
        placeholder=' example : jazz, rap...',
        help='Type in hashtag of a specific challenge')
    if st.button('Search hashtag'):
        display_hashtag_data(tag_type)

with tab5:
    # Music search page
    st.title('Music Data')
    music_type = st.text_input(
        'Search for music',
        placeholder=' example : https://www.tiktok.com/@ayanakamura/video/7190099178314386693...',
        help='Type in url of a TikTok')
    if st.button('Search music'):
        display_music_data(music_type)
