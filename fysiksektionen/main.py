from mattermostdriver import Driver
from threading import Thread
import json

from secret import TOKEN
from configuration import *
from ws import WebSocket


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

def remove_channel_member(driver: Driver, channel, user_id, users_in_channels):
    driver.channels.remove_channel_member(COURSE_CHANNEL_IDS[channel], user_id)
    users_in_channels[channel].remove(user_id)

def add_channel_member(driver: Driver, channel, user_id, users_in_channels):
    driver.channels.add_user(COURSE_CHANNEL_IDS[channel], {"user_id": user_id})
    users_in_channels[channel].add(user_id)

def get_channel_members(driver: Driver, channel, channel_id, users_in_channels):
    users_in_channels[channel] = { user["user_id"] for user in driver.channels.get_channel_members(channel_id) }

def manage_channel_categories(driver: Driver, user_id, team_id):
    # make sure this happens AFTER the user has been added to the relevant categories
    categories = mm_channels_get_user_sidebar_categories(driver, user_id, team_id)["categories"]

    channel_ids = [CHANNELS[channel] for channel in CHANNELS]

    course_category_name = "Fysiksektionen"

    for category in categories:
        if category["display_name"] == course_category_name:
            break
    else:
        mm_channels_create_user_sidebar_category(driver, user_id, team_id, 
                                                 { 
                                                  "user_id": user_id, 
                                                  "team_id": team_id, 
                                                  "display_name": course_category_name, 
                                                  "type": "custom"
                                                  }
                                                 )
        categories = mm_channels_get_user_sidebar_categories(driver, user_id, team_id)["categories"]

    new_categories = []
    for category in categories:
        if category["display_name"] == course_category_name:
            if not all(channel_id in category["channel_ids"] for channel_id in channel_ids):
                new_categories.append({
                    "id": category["id"],
                    "display_name": category["display_name"],
                    "user_id": user_id,
                    "team_id": team_id,
                    "channel_ids": list(set(channel_ids) | set(category["channel_ids"]))
                    })
        else:
            if any(channel_id in category["channel_ids"] for channel_id in channel_ids):
                new_categories.append({
                    "id": category["id"],
                    "display_name": category["display_name"],
                    "user_id": user_id,
                    "team_id": team_id,
                    "channel_ids": [channel_id for channel_id in category["channel_ids"] if channel_id not in channel_ids]
                    })

    if new_categories:
        mm_channels_update_user_sidebar_categories(driver, user_id, team_id, new_categories)

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

        manage_channel_categories(driver, data["user_id"], TEAM_ID)

def delete_new_posts_in_clean_channels(driver: Driver):
    for channel in CHANNELS:
        res = driver.posts.get_posts_for_channel(channel_id = CHANNELS[channel])
            if res["posts"][post]["type"] == "system_add_to_channel":
                print(f"Deleting {post}")
                driver.posts.delete_post(post_id = post)

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

    cc = CourseChannels(driver)

    ws.subscribe("user_added", lambda data: add_to_default_channels(driver, data))

    delete_new_posts_in_clean_channels(driver)

    # User addad to team -> Add to channel {'event': 'user_added', 'data': {'team_id': 'g16tqepa3ffntkfnnwqyapkzkr', 'user_id': 'zu7i4ow3obfa3egwpau59r6s4a'}, 'broadcast': {'omit_users': None, 'user_id': '', 'channel_id': '8e9yhhagtjbnpdyr6eiox8i3oa', 'team_id': '', 'connection_id': ''}, 'seq': 8}

if __name__ == "__main__":
    main()
