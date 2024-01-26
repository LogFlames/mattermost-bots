from threading import Thread
import json
import os
import re

from eliasmamo_import import *
from secret import TOKEN
from configuration import *

def handle_posted(driver: Driver, data, channels):
    if data["channel_type"] != "D": # We only care about replies in DMs
        return

    post = json.loads(data["post"])

    if post["user_id"] == driver.client.userid:
        return

    if post["root_id"]:
        return

    command = post["message"].strip().lower()

    if re.match(r"^join [a-z0-9]{6} [0-9]{5}$", command) is None:
        send_dm(driver, post["user_id"], """Could not parse command, please write on the form
```
join [education code] [instance code]
Example:
join SF1679 60215
```
The education code (utbildningskod) and instance code (tillfälleskod) can be found on [student.ladok.se](https://student.ladok.se). If you encounter any problems please concact [mattermost@f.kth.se](mailto:mattermost@f.kth.se) or DM @ellundel or @eskilny.
""")
        return

    education_code = command[5:11]
    instance_code = command[12:17]

    added_to_channel = ""
    for channel in channels:
        if channel.startswith(education_code) and channel.endswith(instance_code):
            driver.channels.add_user(channels[channel], {"user_id": post["user_id"]})
            with open(os.path.join(os.path.dirname(__file__), "added_to_channel", f"{education_code}-{instance_code}.txt"), "a") as f:
                f.write(f"{post['user_id']}\n")

            added_to_channel = channels[channel]
            break
    else:
        send_dm(driver, post["user_id"], f"""Could not find any channel with education code {education_code} and instance code {instance_code}. Active courses are synced once per study period. Please contact [mattermost@f.kth.se](mailto:mattermost@f.kth.se) or DM @ellundel or @eskilny by DM to create the channel.""")
        return

    delete_new_posts_in_clean_channels(driver, {added_to_channel: added_to_channel})
    send_dm(driver, post["user_id"], """You have been added to the channel.""")

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

    channels = {}
    for channel in get_all_private_channels(driver, TEAM_ID):
        if channel["creator_id"] == driver.client.userid:
            channels[channel["name"]] = channel["id"]

    ws = WebSocket(TOKEN)

    ws.subscribe("posted", lambda data: handle_posted(driver, data, channels))
    print("Listening for new DMs...")

    ws.join()

if __name__ == "__main__":
    main()
