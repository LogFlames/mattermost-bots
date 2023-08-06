from mattermostdriver import Driver
from threading import Thread

def mm_channels_create_user_sidebar_category(driver: Driver, user_id, team_id, options=None):
    return driver.client.post(
        '/users/' + user_id + '/teams/' + team_id + '/channels/categories',
        options=options
    )

def mm_channels_get_user_sidebar_categories(driver: Driver, user_id, team_id):
    return driver.client.get(
        '/users/' + user_id + '/teams/' + team_id + '/channels/categories'
    )

def mm_channels_update_user_sidebar_categories(driver: Driver, user_id, team_id, options=None):
    return driver.client.put(
        '/users/' + user_id + '/teams/' + team_id + '/channels/categories',
        options=options
    )

def mm_channels_delete_user_sidebar_category(driver: Driver, user_id, team_id, category_id):
    return driver.client.delete(
        '/users/' + user_id + '/teams/' + team_id + '/channels/categories/' + category_id
    )

def get_team_members(driver: Driver, team):
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

def delete_new_posts_in_clean_channels(driver: Driver, channels):
    for channel in channels:
        res = driver.posts.get_posts_for_channel(channel_id = channels[channel])
        for post in res["posts"]:
            if res["posts"][post]["type"] in ("system_add_to_channel", "system_join_channel"):
                print(f"Deleting {post}")
                driver.posts.delete_post(post_id = post)

def add_to_default_channels(driver: Driver, wsdata, team_id, channels):
    if wsdata["team_id"] == team_id:
        threads = []
        for channel in channels:
            thread = Thread(target = driver.channels.add_user, args = (channels[channel], {"user_id": wsdata["user_id"]}))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        delete_new_posts_in_clean_channels(driver, channels)
