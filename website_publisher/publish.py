import base64
import requests
import datetime

from typing import Literal

from secret import WP_AUTH
from configuration import FEATURED_MEDIA

def create_wp_post(namnd, title, message, timestamp=None, lang: Literal["sv", "en"] = "sv", status: Literal["draft", "publish"] = "publish"):
    if namnd not in WP_AUTH:
        return 401, {"error": "Must be a valid nämnd from WP_AUTH"}

    url = "https://f.kth.se/wp-json/wp/v2"
    wp_connection = WP_AUTH[namnd]["user"] + ":" + WP_AUTH[namnd]["wp_key"]
    token = base64.b64encode(wp_connection.encode())

    headers = {
            "Authorization": "Basic " + token.decode("utf-8")
            }

    body = {
            "title": title,
            "content": message,
            "status": status,
            "lang": lang
            }

    if timestamp:
        body["date_gmt"] = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%S")

    if namnd in FEATURED_MEDIA:
        body["featured_media"] = FEATURED_MEDIA[namnd]

    print(f"Creating new post with title {title}")
    res = requests.post(url + "/posts", data = body, headers = headers)
    return res.status_code, res.json()

def update_wp_post(namnd, postid, title = None, message = None, featured_media = None, status: Literal["draft", "publish", None] = None):
    if namnd not in WP_AUTH:
        return 401, {"error": "Must be a valid nämnd from WP_AUTH"}

    url = "https://f.kth.se/wp-json/wp/v2"
    wp_connection = WP_AUTH[namnd]["user"] + ":" + WP_AUTH[namnd]["wp_key"]
    token = base64.b64encode(wp_connection.encode())

    headers = {
            "Authorization": "Basic " + token.decode("utf-8")
            }

    body = {}
    if title is not None: body["title"] = title
    if message is not None: body["content"] = message
    if status is not None: body["status"] = status
    if featured_media is not None: body["featured_media"] = featured_media

    print(f"Updating post {postid} with title {title}")
    res = requests.post(url + f"/posts/{postid}", data = body, headers = headers)
    return res.status_code, res.json()

def get_wp_posts(namnd):
    if namnd not in WP_AUTH:
        return 401, {"error": "Must be a valid nämnd from WP_AUTH"}

    url = "https://f.kth.se/wp-json/wp/v2"
    wp_connection = WP_AUTH[namnd]["user"] + ":" + WP_AUTH[namnd]["wp_key"]
    token = base64.b64encode(wp_connection.encode())

    headers = {
            "Authorization": "Basic " + token.decode("utf-8")
            }

    print(f"Getting posts for {namnd}")
    res = requests.get(url + f"/posts", headers = headers)
    return res.status_code, res.json()
