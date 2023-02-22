import subprocess
import json
import pandas as pd
import requests,ast, re
from bs4 import BeautifulSoup

js_file = './call.js'


def fetch_top_influencers(country_code='fr'):
    """
    Returns dataframe of top influencers of the TikTok platform per country
    Parameters
    -------
    country_code : string
        country of the ranking searched (France : 'fr', USA : 'us', UK = 'gb', Germany : 'de'...)
    Returns
    -------
    df_influencers : list
        dataframe of influencers scrapped on designated website (Tokfleunce)
    """

    URL = "https://tokfluence.com/top?limit=100&country=" + country_code
    page = requests.get(URL)

    # fetch list of influencers on main page website
    soup = BeautifulSoup(page.content)
    json_data = soup.find('script', text=re.compile("__NEXT_DATA__"))
    data = str(json_data)[str(json_data).find('__NEXT_DATA__ = '):str(json_data).find('module={}')]
    data = data.replace('__NEXT_DATA__ = ', '')
    list_influencers = '[' + ((data.split('['))[1].split(']')[0]) + ']'

    # convert data to dataframe
    list_influencers = ast.literal_eval(list_influencers)
    df_influencers = pd.DataFrame.from_records(list_influencers)
    df_influencers = df_influencers[
        ['fullName', 'username', '_id', 'uid', 'videosCount', 'followerCount', 'likesCount', 'profilePicUrl', 'region']]

    return df_influencers


def user(username):
    output = subprocess.check_output(f'node -e "require(\'{js_file}\').get_user(\'{username}\')"', shell=True)
    json_out = json.loads(output.decode())
    return json_out


def user_videos(username):
    output = subprocess.check_output(f'node -e "require(\'{js_file}\').get_user_videos(\'{username}\')"', shell=True)
    json_out = json.loads(output.decode())
    return json_out


def hashtag(tag):
    output = subprocess.check_output(f'node -e "require(\'{js_file}\').get_hashtag(\'{tag}\')"', shell=True)
    json_out = json.loads(output.decode())
    return json_out


def music(url):
    output = subprocess.check_output(f'node -e "require(\'{js_file}\').get_music(\'{url}\')"', shell=True)
    json_out = json.loads(output.decode())
    return json_out
