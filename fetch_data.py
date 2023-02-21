import subprocess
import json

js_file = './call.js'


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
