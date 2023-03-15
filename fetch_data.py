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
    result = subprocess.run(f'node -e "require(\'{js_file}\').get_user(\'{username}\')"', capture_output=True, text=True)
    try:
        json_out = json.loads(result.stdout)
        return json_out
    except subprocess.CalledProcessError as e:
        raise e


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
    result = subprocess.run(f'node -e "require(\'{js_file}\').get_user_videos(\'{username}\')"', capture_output=True, text=True)
    try:
        json_out = json.loads(result.stdout)
        return json_out
    except subprocess.CalledProcessError as e:
        raise e


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
    result = subprocess.run(f'node -e "require(\'{js_file}\').get_hashtag(\'{tag}\')"', capture_output=True, text=True)
    try:
        json_out = json.loads(result.stdout)
        return json_out
    except subprocess.CalledProcessError as e:
        raise e


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
    result = subprocess.run(f'node -e "require(\'{js_file}\').get_music(\'{url}\')"', capture_output=True, text=True)
    try:
        json_out = json.loads(result.stdout)
        return json_out
    except subprocess.CalledProcessError as e:
        raise e
