from eliasmamo_import import *
from secret import TOKEN
import json
import tqdm

def new_user(driver: Driver, data):
    if data["channel_name"] == "town-square":
        return

    post = json.loads(data["post"])
    if post["type"] not in ("system_add_to_channel", "system_join_channel"):
        return

    if "props" in post and "addedUserId" in post["props"] and post["props"]["addedUserId"] == driver.client.userid:
        users = get_all_channel_members(driver, post["channel_id"])
        for user in users:
            only_notify_mentions_for_channel(driver, channel_id = post["channel_id"], user_id = user["user_id"])
    else:
        only_notify_mentions_for_channel(driver, post["channel_id"], post["user_id"])

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

    ws = WebSocket(TOKEN)

    ws.subscribe("posted", lambda data: new_user(driver, data))

    print("Setup done. Listening for new posts and reactions...")

    if False:
        todos = []
        teams = driver.teams.get_user_teams(driver.client.userid)
        for team in teams:
            channels = driver.channels.get_channels_for_user(driver.client.userid, team_id = team["id"])
            for channel in channels:
                users = get_all_channel_members(driver, channel["id"])
                if channel["name"] == "town-square":
                    continue
                for user in users:
                    todos.append({"channel": channel["id"], "user": user["user_id"]})

        for todo in tqdm.tqdm(todos):
            only_notify_mentions_for_channel(driver, channel_id = todo["channel"], user_id = todo["user"])

        print("Updated notification props for all users in all channels.")

    ws.join()

if __name__ == "__main__":
    main()
