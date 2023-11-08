from threading import Thread
import json
import os

from eliasmamo_import import *
from secret import TOKEN
from configuration import *

FSN_TEAM = "419spm3ugf8axc8chupqw9e5bo"

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

    for channel in driver.teams.get_public_channels(FSN_TEAM):
        print(f'"{channel["name"]}": "{channel["id"]}",')

    #for ch in driver.channels.get_public_channels(TEAM_ID):
    #    print(f'"{ch["name"]}": "{ch["id"]}",')

if __name__ == "__main__":
    main()
