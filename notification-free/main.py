from eliasmamo_import import *
from secret import TOKEN
import json
import tqdm

def channel_member_updated(driver: Driver, data):
    channel_member = json.loads(data["channelMember"])
    if channel_member['user_id'] != driver.client.userid:
        return

    if "channel_admin" in channel_member["roles"]:
        print(f"Was made channel admin, making all users notification free")
        users = get_all_channel_members(driver, channel_member["channel_id"])
        for user in tqdm.tqdm(users):
            if user["user_id"] == driver.client.userid:
                continue
            only_notify_mentions_for_channel(driver, channel_id = channel_member["channel_id"], user_id = user["user_id"])
    else:
        print(f"Was removed as channel admin, making all users full notification")
        users = get_all_channel_members(driver, channel_member["channel_id"])
        for user in tqdm.tqdm(users):
            if user["user_id"] == driver.client.userid:
                continue
            full_notifications_for_channel(driver, channel_id = channel_member["channel_id"], user_id = user["user_id"])

def new_user(driver: Driver, data):
    if data["channel_name"] == "town-square":
        return

    post = json.loads(data["post"])
    if post["type"] not in ("system_add_to_channel", "system_join_channel"):
        return

    me = driver.channels.get_channel_member(data["channel-id"], driver.client.userid)
    if "channel_admin" not in me["roles"]:
        return 

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
    ws.subscribe("channel_member_updated", lambda data: channel_member_updated(driver, data))

    print("Setup done. Listening for new posts and reactions...")

    if False:
        todos = []
        teams = driver.teams.get_user_teams(driver.client.userid)
        for team in teams:
            channels = driver.channels.get_channels_for_user(driver.client.userid, team_id = team["id"])
            for channel in channels:
                if channel["name"] == "town-square":
                    continue

                me = driver.channels.get_channel_member(channel["id"], driver.client.userid)

                users = get_all_channel_members(driver, channel["id"])

                for user in users:
                    if user["user_id"] == driver.client.userid:
                        continue
                    todos.append({"channel": channel["id"], "user": user["user_id"], "notification_free": "channel_admin" in me["roles"]})

        for todo in tqdm.tqdm(todos):
            if todo["notification_free"]:
                only_notify_mentions_for_channel(driver, channel_id = todo["channel"], user_id = todo["user"])
            else:
                full_notifications_for_channel(driver, channel_id = todo["channel"], user_id = todo["user"])

        print("Updated notification props for all users in all channels.")

    ws.join()

if __name__ == "__main__":
    main()
