from mattermostdriver import Driver
from threading import Thread

from secret import TOKEN
from configuration import *
from ws import WebSocket

def add_to_default_channels(driver: Driver, data):
    if data["team_id"] == TEAM_ID:
        threads = []
        for channel in CHANNELS:
            thread = Thread(target = driver.channels.add_user, args = (CHANNELS[channel], {"user_id": data["user_id"]}))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        delete_new_posts_in_clean_channels(driver)

def delete_new_posts_in_clean_channels(driver: Driver):
    for channel in CHANNELS:
        res = driver.posts.get_posts_for_channel(channel_id = CHANNELS[channel])
        for post in res["posts"]:
            if res["posts"][post]["type"] in ("system_add_to_channel", "system_join_channel"):
                print(f"Deleting {post}")
                driver.posts.delete_post(post_id = post)

def get_team_members(driver, team):
    members = []
    page = 0
    while True:
        mems = driver.teams.get_team_members(team, {"per_page": 200, "page": page})
        for member in mems:
            members.append(member["user_id"])
        if len(mems) == 0:
            break
        page += 1
    return members

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
    ws = WebSocket()

    print("Listening for new users")
    ws.subscribe("user_added", lambda data: add_to_default_channels(driver, data))

    delete_new_posts_in_clean_channels(driver)

    if False:
        print("Adding new users to default channels...")
        for user in get_team_members(driver, TEAM_ID):
            add_to_default_channels(driver, {"team_id": TEAM_ID, "user_id": user})
        print("Adding new users to default channels ... Done")

    # User addad to team -> Add to channel {'event': 'user_added', 'data': {'team_id': 'g16tqepa3ffntkfnnwqyapkzkr', 'user_id': 'zu7i4ow3obfa3egwpau59r6s4a'}, 'broadcast': {'omit_users': None, 'user_id': '', 'channel_id': '8e9yhhagtjbnpdyr6eiox8i3oa', 'team_id': '', 'connection_id': ''}, 'seq': 8}

if __name__ == "__main__":
    main()
