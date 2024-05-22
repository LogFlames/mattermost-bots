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

    disable_notifications_for_channel(driver, post["channel_id"], post["user_id"])

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

    teams = driver.teams.get_user_teams(driver.client.userid)
    for team in tqdm.tqdm(teams):
        channels = driver.channels.get_channels_for_user(driver.client.userid, team_id = team["id"])
        for channel in channels:
            users = get_all_channel_members(driver, channel["id"])
            if channel["name"] == "town-square":
                continue
            for user in users:
                disable_notifications_for_channel(driver, channel_id = channel["id"], user_id = user["user_id"])

        print("Updated notification props for all users in all channels.")

    ws.join()

if __name__ == "__main__":
    main()
