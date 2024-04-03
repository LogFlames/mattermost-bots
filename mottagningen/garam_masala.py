from eliasmamo_import import *
from secret import TOKEN
from mattermostdriver.exceptions import ResourceNotFound

import json
import re

GARAM_SKICK_CHANNEL_ID = "8yi6h57ynpf7p8stumxrxzuqdo"
GARAM_MASALA_GROUP_ID = "fwfa45hs73n4fj6bw5yabsm1wc"

def new_post(driver: Driver, data):
    if "post" not in data:
        return

    post = json.loads(data["post"])

    if post["channel_id"] != GARAM_SKICK_CHANNEL_ID:
        return

    if post["user_id"] == driver.client.userid:
        return

    if post["root_id"] != "":
        return

    username = post["message"].strip()

    if re.match("^@[a-z-_]*$", username) is None:
        driver.posts.create_post({"channel_id": GARAM_SKICK_CHANNEL_ID, "message": "Unexpected format, please write on the form `@username`", "root_id": post["id"]})
        return

    try:
        user = driver.users.get_user_by_username(username[1:])
    except ResourceNotFound:
        print(f"Could not find user with username '{username}'")
        driver.posts.create_post({"channel_id": GARAM_SKICK_CHANNEL_ID, "message": f"Could not find user with username '{username}'. Make sure it is spelled correctly.", "root_id": post["id"]})
        return

    print(f"Setting @garam-masala to user '{username}'")

    group_members = mm_custom_group_get_members(driver, GARAM_MASALA_GROUP_ID)
    user_ids_to_remove = [member["id"] for member in group_members["members"]]
    mm_custom_group_remove_members(driver, GARAM_MASALA_GROUP_ID, user_ids_to_remove)
    mm_custom_group_add_members(driver, GARAM_MASALA_GROUP_ID, [user["id"]])

    driver.posts.create_post({"channel_id": GARAM_SKICK_CHANNEL_ID, "message": f"Moved @garam-masala to {username}", "root_id": post["id"]})

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

    print("Listening for new posts in garam-skick channel")
    ws.subscribe("posted", lambda data: new_post(driver, data))

    ws.join()

if __name__ == "__main__":
    main()
