import requests

URL = "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en"
page = requests.get(URL)

print(page.text)
