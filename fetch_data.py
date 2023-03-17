import json
import subprocess

js_file = './scrap_tiktok'


def user(username):
    """
    Returns dictionary of information of a TikTok user

    Parameters
    -------
    username : string
        unique username of user
    Returns
    -------
    json_out : json_out
        json of user fetched with the TikTok signature API
    """
    output = subprocess.check_output(f'node -e "require(\'{js_file}\').get_user(\'{username}\')"', shell=True)
    json_out = json.loads(output.decode())
    return json_out


def user_videos(username):
    """
    Returns list of videos of a user

    Parameters
    -------
    username : string
        unique username of user
    Returns
    -------
    json_out : json_out
        json of videos fetched with the TikTok signature API
    """
    output = subprocess.check_output(f'node -e "require(\'{js_file}\').get_user_videos(\'{username}\')"', shell=True)
    json_out = json.loads(output.decode())
    return json_out


def hashtag(tag):
    """
    Returns list of videos of a hashtag

    Parameters
    -------
    tag : string
        name of a challenge
    Returns
    -------
    json_out : json_out
        json of videos fetched with the TikTok signature API
    """
    output = subprocess.check_output(f'node -e "require(\'{js_file}\').get_hashtag(\'{tag}\')"', shell=True)
    json_out = json.loads(output.decode())
    return json_out


def music(url):
    """
    Returns list of videos of a music

    Parameters
    -------
    url : string
        url of a music associated to any TikTok
    Returns
    -------
    json_out : json_out
        json of videos fetched with the TikTok signature API
    """
    output = subprocess.check_output(f'node -e "require(\'{js_file}\').get_music(\'{url}\')"', shell=True)
    json_out = json.loads(output.decode())
    return json_out
