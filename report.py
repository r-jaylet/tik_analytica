import streamlit as st

from fetch_data import user, user_videos, hashtag, music


def display_user_data(username_):
    json_user = user(username_)
    st.write(json_user)

    df_user = user_videos(username_)
    st.write(df_user)


def display_hashtag_data(tag_):
    df_hash = hashtag(tag_)
    st.write(df_hash)


def display_music_data(music_):
    df_music = music(music_)
    st.write(df_music)


# Set the page title
st.set_page_config(page_title='Data Search', page_icon=':bar_chart:', layout='wide')

# Add the three buttons
category = st.sidebar.radio('Select a Category:', ('User', 'Hashtag', 'Music'))

if category == 'User':
    st.title('User Data')
    user_type = st.text_input('Enter the username:')
    if st.button('Search'):
        display_user_data(user_type)

elif category == 'Hashtag':
    st.title('Hashtag Data')
    tag_type = st.text_input('Enter the hashtag:')
    if st.button('Search'):
        display_hashtag_data(tag_type)

else:
    st.title('Music Data')
    music_type = st.text_input('Enter the music name:')
    if st.button('Search'):
        display_music_data(music_type)
