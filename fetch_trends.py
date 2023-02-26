import json
import pandas as pd
import requests
from bs4 import BeautifulSoup


def fetch_top_trends():
    url = f"https://ads.tiktok.com/business/creativecenter/trends/home/pc/en"
    page = requests.get(url)
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

    hashtag_content = json_content['hashtags']
    music_content = json_content['trendMusic']
    creator_content = json_content['creatorList']
    tiktok_content = json_content['tiktoks']

    hashtag = hashtag.merge(pd.DataFrame.from_records(hashtag_content), left_index=True, right_index=True)
    music = music.merge(pd.DataFrame.from_records(music_content), left_index=True, right_index=True)
    creator = creator.merge(pd.DataFrame.from_records(creator_content), left_index=True, right_index=True)
    tiktok = pd.DataFrame.from_records(tiktok_content)

    hashtag['creators_examples'] = hashtag.apply(lambda x: ([e['nickName'] for e in x['creators']]), axis=1)
    hashtag = hashtag[['rank', 'tag', 'posts_count', 'views_count', 'creators_examples']].set_index('rank')
    music = music[['rank', 'music', 'author', 'countryCode', 'cover', 'link', 'urlTitle', 'songId']].set_index('rank')
    creator['rank'] = [1, 2, 3, 4, 5]
    creator = creator[['creator', 'followers_count', 'likes_count',
                       'countryCode', 'userId', 'ttLink', 'rank']].set_index('rank')
    tiktok['rank'] = [1, 2, 3, 4, 5]
    tiktok = tiktok[['id', 'title', 'countryCode', 'duration', 'itemUrl', 'cover', 'rank']].set_index('rank')

    return hashtag, music, creator, tiktok


def hashtag_trend_info(hashtag, country, period):
    url = f'https://ads.tiktok.com/business/creativecenter/hashtag/{hashtag}/pc/en' \
          f'?countryCode={country}&period={period}'
    page = requests.get(url)

    soup = BeautifulSoup(page.text)

    stats = [e.text for e in soup.find_all('span', {'class': 'title--gvWft title--eM6Wz'})]
    trend = soup.find('span', {'class': 'bannerDesc--CORuD bannerDesc--McarQ'}).text
    region_info = []
    region = soup.find_all('div', {'class': 'content-wrap-item--P88lK content-wrap-item--zMoGF'})
    for r in region:
        reg = {'country': r.find('span', {'class': 'content-wrap-item-label-wrap-label--33mdU '
                                                   'content-wrap-item-label-wrap-label--uojf9'}).text,
               'count': r.find('span', {'class': 'content-wrap-item-value-wrap-value--wtBCS '
                                                 'content-wrap-item-value-wrap-value--q-PNh'}).text}
        region_info.append(reg)
    related_hashtags = [h.find('span').text for h in soup.find_all('div', {'class': 'mtitle--EtrCY mtitle--mJqfP'})]

    region_info = pd.DataFrame(region_info)
    related_hashtags = pd.DataFrame(related_hashtags)

    return stats, trend, region_info, related_hashtags


def music_trend_info(song, country, period):
    url = f"https://ads.tiktok.com/business/creativecenter/song/{song}/pc/en?countryCode={country}&period={period}"
    page = requests.get(url)

    soup = BeautifulSoup(page.text)

    trend = soup.find('span', {'class': 'bannerDesc--yWTb+ bannerDesc--94fZk'}).text
    region_info = []
    region = soup.find_all('div', {'class': 'content-wrap-item--P88lK content-wrap-item--zMoGF'})
    for r in region:
        reg = {'country': r.find('span', {
            'class': 'content-wrap-item-label-wrap-label--33mdU'
                     'content-wrap-item-label-wrap-label--uojf9'}).text,
               'count': r.find('span', {
                   'class': 'content-wrap-item-value-wrap-value--wtBCS'
                            'content-wrap-item-value-wrap-value--q-PNh'}).text}
        region_info.append(reg)
    sounds = soup.find_all('div', {'class': 'soundItem--OBPhW soundItem--IE6BO'})
    music_info = []
    for s in sounds:
        music = {'name': s.find('span', {'class': 'soundItem-desc-title--Zu0RR soundItem-desc-title--skY+6'}).text,
                 'artist': s.find('span', {'class': 'soundItem-desc-author--QMtpm soundItem-desc-author--x-lDq'}).text}
        music_info.append(music)

    region_info = pd.DataFrame(region_info)
    music_info = pd.DataFrame(music_info)

    return trend, region_info, music_info
