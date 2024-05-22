from eliasmamo_import import *
from secret import TOKEN
import json
import tqdm

def handle_posted(driver: Driver, data):
    post = json.loads(data["post"])
    if post["type"] not in ("system_add_to_channel", "system_join_channel", "system_remove_from_channel", "system_leave_channel"):
        return

    if "props" in post and "addedUserId" in post["props"] and post["props"]["addedUserId"] == driver.client.userid:
        res = driver.posts.get_posts_for_channel(post["channel_id"])
        for p in res["posts"]:
            if res["posts"][p]["type"] in ("system_add_to_channel", "system_join_channel", "system_remove_from_channel", "system_leave_channel"):
                driver.posts.delete_post(post_id = p)
    else:
        driver.posts.delete_post(post["id"])

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

    ws.subscribe("posted", lambda data: handle_posted(driver, data))

    print("Setup done. Listening for new posts and reactions...")

    teams = driver.teams.get_user_teams(driver.client.userid)
    for team in tqdm.tqdm(teams):
        channels = driver.channels.get_channels_for_user(driver.client.userid, team_id = team["id"])
        for channel in channels:
            res = driver.posts.get_posts_for_channel(channel["id"])
            for post in res["posts"]:
                if res["posts"][post]["type"] in ("system_add_to_channel", "system_join_channel", "system_remove_from_channel", "system_leave_channel"):
                    print(f"Deleting system join post: {post}")
                    driver.posts.delete_post(post_id = post)

    print("Removed all join/leave massages from channels the bot is in.")

    ws.join()

if __name__ == "__main__":
    main()
