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

def manage_channel_categories(driver: Driver, user_id, team_id, channels, conf_categories):
    # make sure this happens AFTER the user has been added to the relevant categories
    categories = mm_channels_get_user_sidebar_categories(driver, user_id, team_id)["categories"]


    for required_category in conf_categories:
        for category in categories:
            if category["display_name"] == required_category:
                break
        else:
            mm_channels_create_user_sidebar_category(driver, user_id, team_id, 
                                                     { 
                                                      "user_id": user_id, 
                                                      "team_id": team_id, 
                                                      "display_name": required_category, 
                                                      "type": "custom"
                                                      }
                                                     )
            categories = mm_channels_get_user_sidebar_categories(driver, user_id, team_id)["categories"]

    channel_ids = []
    for category_name in conf_categories:
        channel_ids.extend([channels[channel_name] for channel_name in conf_categories[category_name]])

    new_categories = []
    for category in categories:
        should_have_channels = set(category["channel_ids"])
        should_have_channels -= {*channel_ids}

        for category_name in conf_categories:
            if category_name == category["display_name"]:
                should_have_channels |= {channels[channel_name] for channel_name in conf_categories[category_name]}

        if should_have_channels != set(category["channel_ids"]):
            new_categories.append({
                "id": category["id"],
                "display_name": category["display_name"],
                "user_id": user_id,
                "team_id": team_id,
                "channel_ids": [channel_id for channel_id in should_have_channels]
                })
    if new_categories:
        mm_channels_update_user_sidebar_categories(driver, user_id, team_id, new_categories)

def mm_custom_group_add_members(driver: Driver, group_id, user_ids):
    return driver.client.post(
        '/groups/' + group_id + '/members',
        options={"user_ids": user_ids}
    )

def mm_custom_group_remove_members(driver: Driver, group_id, user_ids):
    return driver.client.delete(
        '/groups/' + group_id + '/members',
        options = {"user_ids": user_ids}
    )

def mm_custom_group_get_members(driver: Driver, group_id, page = 0, per_page = 60):
    return driver.client.get(
        '/groups/' + group_id + '/members',
        params = {"page": page, "per_page": per_page}
    )

def get_channel_members(driver: Driver, channel_id):
    members = []
    page = 0
    while True:
        mems = driver.channels.get_channel_members(channel_id, {"per_page": 200, "page": page})
        for member in mems:
            members.append(member["user_id"])
        if len(mems) == 0:
            break
        page += 1
    return members

def get_team_members(driver: Driver, team_id):
    members = []
    page = 0
    while True:
        mems = driver.teams.get_team_members(team_id, {"per_page": 200, "page": page})
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
            if res["posts"][post]["type"] in ("system_add_to_channel", "system_join_channel", "system_remove_from_channel", "system_leave_channel"):
                print(f"Deleting system join post: {post}")
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

        # delete_new_posts_in_clean_channels(driver, channels)

def only_notify_mentions_for_channel(driver: Driver, channel_id, user_id):
    notify = driver.client.put(
            '/channels/' + channel_id + "/members/" + user_id + "/notify_props")

    notify["desktop"] = "mention"
    notify["desktop_threads"] = "all"
    notify["push"] = "mention"
    notify["push_threads"] = "all"

    return driver.client.put(
        '/channels/' + channel_id + '/members/' + user_id + "/notify_props",
        options = {
            **notify
        }
    )

def full_notifications_for_channel(driver: Driver, channel_id, user_id):
    notify = driver.client.put(
            '/channels/' + channel_id + "/members/" + user_id + "/notify_props")

    notify["desktop"] = "all"
    notify["desktop_threads"] = "all"
    notify["push"] = "all"
    notify["push_threads"] = "all"

    return driver.client.put(
        '/channels/' + channel_id + '/members/' + user_id + "/notify_props",
        options = {
            **notify
        }
    )

def enable_all_notifications(driver: Driver, user_id):
    user_props = driver.client.put(
            '/users/' + user_id + "/patch")

    notify = user_props["notify_props"]
    notify["channel"] = "true"
    notify["desktop"] = "all"
    notify["desktop_threads"] = "all"
    notify["first_name"] = "true"
    notify["push"] = "all"
    notify["push_status"] = "online"
    notify["push_threads"] = "all"

    return driver.client.put(
        '/users/' + user_id + '/patch',
        options = {
            "notify_props": notify
        }
    )

def send_dm(driver: Driver, userid, message, root_id=None):
    dm_channel = driver.channels.create_direct_message_channel([userid, driver.client.userid])
    post_data = {"channel_id": dm_channel["id"], "message": message}
    if root_id:
        post_data["root_id"] = root_id
    driver.posts.create_post(post_data)

def get_all_users(driver: Driver):
    users = []
    page = 0
    new_users = [None]
    while len(new_users) > 0:
        new_users = driver.users.get_users({"page": page, "per_page": 100})
        users.extend(new_users)
        page += 1

    return users

def get_all_channel_members(driver: Driver, channel_id):
    users = []
    page = 0
    new_users = [None]
    while len(new_users) > 0:
        new_users = driver.channels.get_channel_members(channel_id = channel_id, params = {"page": page, "per_page": 100})
        users.extend(new_users)
        page += 1

    return users

def get_all_public_channels(driver: Driver, team_id):
    channels = []
    page = 0
    new_channels = [None]
    while len(new_channels) > 0:
        new_channels = driver.channels.get_public_channels(team_id, {"page": page, "per_page": 60})
        channels.extend(new_channels)
        page += 1

    return channels

def get_all_private_channels(driver: Driver, team_id):
    channels = []
    page = 0
    new_channels = [None]
    while len(new_channels) > 0:
        new_channels = driver.client.get(
                endpoint = f"/teams/{team_id}/channels/private",
                params = {"page": page, "per_page": 60})
        channels.extend(new_channels)
        page += 1

    return channels

def send_post_as_other_user(driver: Driver, user_id, channel_id, message, root_id=""):
    token = driver.users.create_user_access_token(user_id, {"description": "Send as other user - Bot"})
    driver_other = Driver(
            {
                'url': 'mattermost.fysiksektionen.se',
                'basepath': '/api/v4',
                'verify': True,
                'scheme': 'https',
                'port': 443,
                'auth': None,
                'token': token["token"],
                'keepalive': True,
                'keepalive_delay': 5,
                }
            )

    driver_other.login()

    driver_other.posts.create_post({"channel_id": channel_id, "message": message, "root_id": root_id})

    driver.users.disable_personal_access_token({"token_id": token["id"]})

def send_dm_as_other_user(driver: Driver, from_userid, to_userid, message, root_id=None):
    dm_channel = driver.channels.create_direct_message_channel([from_userid, to_userid])
    post_data = {"channel_id": dm_channel["id"], "message": message}
    if root_id:
        post_data["root_id"] = root_id

    token = driver.users.create_user_access_token(from_userid, {"description": "Send as other user - Bot"})
    driver_other = Driver(
            {
                'url': 'mattermost.fysiksektionen.se',
                'basepath': '/api/v4',
                'verify': True,
                'scheme': 'https',
                'port': 443,
                'auth': None,
                'token': token["token"],
                'keepalive': True,
                'keepalive_delay': 5,
                }
            )

    driver_other.login()

    post = driver_other.posts.create_post(post_data)

    driver.users.disable_personal_access_token({"token_id": token["id"]})

    return post
