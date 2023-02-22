import subprocess
import json
import pandas as pd
import requests, ast, re
from bs4 import BeautifulSoup


def fetch_top_trends():
    URL = f"https://ads.tiktok.com/business/creativecenter/trends/home/pc/en"
    page = requests.get(URL)
    soup = BeautifulSoup(page.text)

    trending_hashtag = []
    trending_music = []
    trending_creator = []

    for s in soup.find_all('div', id='hashtagItemContainer'):
        tag = s.find('span', {"class": "titleText--qKHbP"}).text
        stats = s.find_all('span', {"class": "item-value--VAdnq"})
        posts = stats[0].text
        views = stats[1].text
        trending_hashtag.append([tag, posts, views])

    for s in soup.find_all('div', {"class": "music-name-wrap--FPaLL music-name-wrap--X6m9u"}):
        trending_music.append(s.text)

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

    hashtags_content = json_content['hashtags']
    tiktoks_content = json_content['tiktoks']
    trendMusic_content = json_content['trendMusic']
    creatorList_content = json_content['creatorList']

    hashtag = hashtag.merge(pd.DataFrame.from_records(hashtags_content), left_index=True, right_index=True)
    music = music.merge(pd.DataFrame.from_records(trendMusic_content), left_index=True, right_index=True)
    creator = creator.merge(pd.DataFrame.from_records(creatorList_content), left_index=True, right_index=True)
    tiktok = pd.DataFrame.from_records(tiktoks_content)

    hashtag['creators_examples'] = hashtag.apply(lambda x: ([e['nickName'] for e in x['creators']]), axis=1)
    hashtag = hashtag[['rank', 'tag', 'posts_count', 'views_count', 'creators_examples']].set_index(
        'rank')
    music = music[
        ['rank', 'music', 'author', 'countryCode', 'cover', 'link', 'urlTitle', 'songId']].set_index('rank')
    creator['rank'] = [1, 2, 3, 4, 5]
    creator = creator[
        ['creator', 'followers_count', 'likes_count', 'countryCode', 'userId', 'ttLink', 'rank']].set_index('rank')
    tiktok['rank'] = [1, 2, 3, 4, 5]
    tiktok = tiktok[['id', 'title', 'countryCode', 'duration', 'itemUrl', 'cover', 'rank']].set_index('rank')

    return hashtag, music, creator, tiktok
