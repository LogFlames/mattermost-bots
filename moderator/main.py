from eliasmamo_import import *
from secret import TOKEN
import json

EVENAMENG_CHANNEL_ID = "wkgnsmmbqpgpj8ptdiyx8os16c"
GENERAL_CHANNEL_ID = "wy6t5d3tapf5pfbgxq9onp1upe"
ADMIN_TEST_CHANNEL_ID = "dcbn8ipq8381bgcwdre78x9skh"

CHANNEL_IDS = [EVENAMENG_CHANNEL_ID, GENERAL_CHANNEL_ID, ADMIN_TEST_CHANNEL_ID]

def get_teams_name(driver: Driver):
    channel_id_to_team_urls = {}
    for channel_id in CHANNEL_IDS:
        channel = driver.channels.get_channel(channel_id)

        team = driver.teams.get_team(channel["team_id"])

        channel_id_to_team_urls[channel_id] = team["name"]

    return channel_id_to_team_urls

def handle_posted(driver: Driver, data, CHANNEL_ID_TO_TEAM_URL):
    post = json.loads(data["post"])

    if post["channel_id"] not in CHANNEL_IDS:
        return

    if post["user_id"] == driver.client.userid:
        return

    if post["root_id"]:
        return

    if not post["message"].startswith("#"):
        mattermost_message_link = f"https://mattermost.fysiksektionen.se/{CHANNEL_ID_TO_TEAM_URL[post['channel_id']]}/pl/{post['id']}"
        send_dm(driver, post["user_id"], f"""### Please include titles in your messages
To increase the readability of posts sent in ~evenemang and ~general, it is very helpful to include a title describing the subject of the message.

In the future, please include a title on the following format:
```markdown
### Title here

Text here...
```

Consider editing in a title in the [message you just sent]({mattermost_message_link}).""")

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

    CHANNEL_ID_TO_TEAM_URL = get_teams_name(driver)

    ws = WebSocket(TOKEN)

    ws.subscribe("posted", lambda data: handle_posted(driver, data, CHANNEL_ID_TO_TEAM_URL))

    print("Setup done. Listening for new posts and reactions...")

    ws.join()

if __name__ == "__main__":
    main()
