import numpy as np
import json
import pandas as pd
import requests
import ast
import re
from bs4 import BeautifulSoup


def fetch_top_trends():
    """
    Returns dataframes of top trends for each category of items on TikTok

    Returns
    -------
    hashtag : dataframe
        dataframe of top trending hashtags scrapped on ads TikTok site
    music : dataframe
        dataframe of top trending musics scrapped on ads TikTok site
    creator : dataframe
        dataframe of top trending creators scrapped on ads TikTok site
    tiktok : dataframe
        dataframe of top trending tiktoks scrapped on ads TikTok site
    """
    url = f'https://ads.tiktok.com/business/creativecenter/trends/home/pc/en'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='lxml')

    trending_hashtag = []
    trending_music = []
    trending_creator = []

    # get hashtag info
    for s in soup.find_all('div', id='hashtagItemContainer'):
        tag = s.find('span', {"class": "titleText--qKHbP"}).text
        stats = s.find_all('span', {"class": "item-value--VAdnq"})
        posts = stats[0].text
        views = stats[1].text
        trending_hashtag.append([tag, posts, views])

    # get music info
    for s in soup.find_all('div', {"class": "music-name-wrap--FPaLL music-name-wrap--X6m9u"}):
        trending_music.append(s.text)

    # get creator info
    for s in soup.find_all('div', id='creatorItemContainer'):
        tag = s.find('span', {"class": "music-name--LR+1s music-name--bEzZ1"}).text
        stats = s.find_all('span', {"class": "creator-data-value--CwFQt creator-data-value--S-K2V"})
        posts = stats[0].text
        views = stats[1].text
        trending_creator.append([tag, posts, views])

    hashtag = pd.DataFrame(trending_hashtag, columns=['tag', 'posts_count', 'views_count'])
    music = pd.DataFrame(trending_music, columns=['music'])
    creator = pd.DataFrame(trending_creator, columns=['creator', 'followers_count', 'likes_count'])

    find_content = soup.find('script', id="__NEXT_DATA__")
    str_content = str(find_content).split('<')[1].split('>')[1]

    json_content = json.loads(str_content)['props']['pageProps']

    if 'data' in json_content.keys():
        json_content = json_content['data']

    hashtag_content = json_content['hashtags']
    music_content = json_content['trendMusic']
    creator_content = json_content['creatorList']
    tiktok_content = json_content['tiktoks']

    # gather all data
    hashtag = hashtag.merge(pd.DataFrame.from_records(hashtag_content), left_index=True, right_index=True)
    music = music.merge(pd.DataFrame.from_records(music_content), left_index=True, right_index=True)
    creator = creator.merge(pd.DataFrame.from_records(creator_content), left_index=True, right_index=True)
    tiktok = pd.DataFrame.from_records(tiktok_content)

    # format info
    hashtag['creators_examples'] = hashtag.apply(lambda x: ([e['nickName'] for e in x['creators']]), axis=1)
    hashtag = hashtag[['rank', 'tag', 'posts_count', 'views_count', 'creators_examples']].set_index('rank')
    music = music[['rank', 'cover', 'music', 'author', 'countryCode', 'songId', 'link']].set_index('rank')
    creator['rank'] = list(np.arange(len(creator)))
    creator = creator[['creator', 'followers_count', 'likes_count',
                       'countryCode', 'userId', 'ttLink', 'rank']].set_index('rank')
    tiktok['rank'] = list(np.arange(len(tiktok)))
    tiktok = tiktok[['id', 'title', 'countryCode', 'duration', 'itemUrl', 'cover', 'rank']].set_index('rank')

    return hashtag, music, creator, tiktok


def hashtag_trend_info(hashtag, country_code, period):
    """
    Returns information on ads TikTok site of a designated hashtag

    Parameters
    -------
    hashtag : string
        name of a challenge
    country_code : string
        id of a country (FR: France)
    period : string
        length of the period of study of the challenge in days (can be : 30, 120, 360)
    Returns
    -------
    stats : list
        list of posts and views statistics of a designated challenge
    trend : string
        information on status of the trend
    trend_graph : dataframe
        evolution of the trend on the period of study
    audience_ages : dataframe
        information on the age of the audience
    audience_countries : dataframe
        information on the country of origin of the audience
    related_hashtags : dataframe
        most commonly used hashtags used with
    related_items : dataframe
        trendy videos that used this specific hashtag
    """
    url = f'https://ads.tiktok.com/business/creativecenter/hashtag/{hashtag}/pc/en' \
          f'?countryCode={country_code}&period={period}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='lxml')
    
    stats = [e.text for e in soup.find_all('span', {'class': 'title--gvWft title--eM6Wz'})]
    trend = soup.find('span', {'class': 'sectionDesc--MeTTU sectionDesc--v0N+l'}).text
    
    find_content = soup.find('script', id="__NEXT_DATA__")
    str_content = str(find_content).split('<')[1].split('>')[1]
    json_content = json.loads(str_content)['props']['pageProps']['data']

    trend_graph = pd.DataFrame.from_records(json_content['trend'])
    trend_graph['time'] = pd.to_datetime(trend_graph.time, unit='s').astype(str)
    audience_ages = pd.DataFrame.from_records(json_content['audienceAges'])
    audience_ages['ageLevel'] = audience_ages['ageLevel'].replace(3, '18-24').replace(4, '25-34').replace(5, '35+')
    audience_countries = pd.DataFrame.from_records(json_content['audienceCountries'])
    audience_countries['countryInfo'] = audience_countries.apply(lambda x: x['countryInfo']['value'], axis=1)
    related_hashtags = pd.DataFrame.from_records(json_content['relatedHashtags'])
    related_items = pd.DataFrame.from_records(json_content['relatedItems'])

    return stats, trend, trend_graph, audience_ages, audience_countries, related_hashtags, related_items


def music_trend_info(song, country_code, period):
    """
    Returns information on ads TikTok site of a designated music

    Parameters
    -------
    song : string
        name and unique_id of a music
    country_code : string
        name of a country
    period : string
        length of the period of study of the challenge in days (can be : 30, 120, 360)
    Returns
    -------
    trend : string
        information on status of the trend
    trend_graph : dataframe
        evolution of the trend on the period of study
    audience_ages : dataframe
        information on the age of the audience
    audience_countries : dataframe
        information on the country of origin of the audience
    related_items : dataframe
        trendy videos that used this specific hashtag
    """
    url = f"https://ads.tiktok.com/business/creativecenter/song/{song}/pc/en?countryCode={country_code}&period={period}"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, features='lxml')

    trend = soup.find('span', {'class': 'sectionDesc--iGpw7 sectionDesc--OJ+RE'}).text

    find_content = soup.find('script', id="__NEXT_DATA__")
    str_content = str(find_content).split('<')[1].split('>')[1]
    json_content = json.loads(str_content)['props']['pageProps']['data']

    trend_graph = pd.DataFrame.from_records(json_content['trend'])
    trend_graph['time'] = pd.to_datetime(trend_graph.time, unit='s').astype(str)
    audience_ages = pd.DataFrame.from_records(json_content['audienceAges'])
    audience_ages['ageLevel'] = audience_ages['ageLevel'].replace(3, '18-24').replace(4, '25-34').replace(5, '35+')
    audience_countries = pd.DataFrame.from_records(json_content['audienceCountries'])
    audience_countries['countryInfo'] = audience_countries.apply(lambda x: x['countryInfo']['value'], axis=1)
    related_items = pd.DataFrame.from_records(json_content['relatedItems'])

    return trend, trend_graph, audience_ages, audience_countries, related_items


def fetch_top_influencers(country_code='fr'):
    """
    Returns dataframe of top influencers of the TikTok platform per country

    Parameters
    -------
    country_code : string
        country of the ranking searched (France : 'fr', USA : 'us', UK = 'gb', Germany : 'de'...)
    Returns
    -------
    df_influencers : dataframe
        dataframe of influencers scrapped on designated website
    """
    url = "https://tokfluence.com/top?limit=100&country=" + country_code
    page = requests.get(url)

    # fetch list of influencers on main page website
    soup = BeautifulSoup(page.content, features='lxml')
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
