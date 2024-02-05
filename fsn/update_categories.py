from threading import Thread
import unicodedata
import openpyxl
import os
import re

from eliasmamo_import import *
from secret import TOKEN
from configuration import TEAM_ID

def main():
    driver = Driver(
            {
                'url': 'mattermost.fysiksektionen.se',
                'basepath': '/api/v4',
                'verify': True,
                'scheme': 'https',
                'port': 443,
                'auth': None,
                'token': TOKEN,
                'keepalive': True,
                'keepalive_delay': 5,
                }
            )

    driver.login()

    users = {}
    for user in get_all_users(driver):
        users[user["username"]] = user["id"]

    channels = {}
    categories = {"Kurser": []}
    for channel in get_all_private_channels(driver, TEAM_ID):
        if channel["creator_id"] == driver.client.userid:
            channels[channel["name"]] = channel["id"]
            if re.match(r"^[a-z0-9]{6}-[a-z-]*-[0-9]{5}$", channel["name"]) is not None:
                categories["Kurser"].append(channel["name"])

    for user in users:
        print(f"Updating categories for user: {user}...")
        manage_channel_categories(driver, users[user], TEAM_ID, channels, categories)

if __name__ == "__main__":
    main()
