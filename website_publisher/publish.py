import base64
import requests

from typing import Literal

from secret import WP_AUTH

def create_wp_post(namnd, title, message, status: Literal["draft", "publish"] = "publish"):
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
            "lang": "sv"
            }

    res = requests.post(url + "/posts", data = body, headers = headers)
    return res.status_code, res.json()

def update_wp_post(namnd, postid, title = None, message = None, status: Literal["draft", "publish", None] = None):
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

    res = requests.post(url + f"/posts/{postid}", data = body, headers = headers)
    return res.status_code, res.json()


