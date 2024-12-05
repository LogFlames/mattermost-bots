# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownLambdaType=false
# pyright: reportUnknownMemberType=false
# pyright: reportUnknownParameterType=false
# pyright: reportUnknownVariableType=false
# pyright: reportAny=false
# pyright: reportMissingParameterType=false

from eliasmamo_import import *
from secret import TOKEN
from configuration import SCHEDULED_MESSAGES_CHANNEL_ID, SCHEDULED_MESSAGES_POST_ID, CHANNEL_KEYWORDS
import json
import datetime
import re

def get_help_text():
    return f"""`yyyy-mm-dd hh:mm` - update the time by typing a timestamp on the format `yyyy-mm-dd hh:mm`. Example: `2024-12-04 12:30`, `2024-02-10 09:00`
`channel_id` - You can update the channel by typing one of the preconfigured channels, `{'`, `'.join(CHANNEL_KEYWORDS.keys())}`, or a channel-id for a custom channel.
`english` - if the channel is `evenemang` or `general` you can type `english` to also send an automatically translated message. You will get the oportunity to edit the translation before sending.
"""

def get_channel_team_name(driver: Driver, channel_id: str):
    channel = driver.channels.get_channel(channel_id)
    team = driver.teams.get_team(channel["team_id"])
    return team["name"]

def get_channel_name(driver: Driver, channel_id: str):
    try:
        channel = driver.channels.get_channel(channel_id)
        return channel["name"]
    except mattermostdriver.exceptions.ResourceNotFound:
        return "<channel not found>" # some function rely on this exact string, change in those places as well, I'm sorry.
    except mattermostdriver.exceptions.InvalidOrMissingParameters:
        return "<invalid or missing channel id>" # some function rely on this exact string, change in those places as well, I'm sorry.


def create_data_table(driver, data):
    table = "| | |\n|---|---|"
    if data["channel_id"]:
        table += f"\n| channel | {get_channel_name(driver, data['channel_id'])} |"
    else:
        table += "\n| channel | <unset> |"

    if data["time"]:
        table += f"\n| time | {data['time']} |"
    else:
        table += "\n| time | <unset> |"

    if data["linked_english_post_id"]:
        table += f"\n| english post | [link to post](https://mattermost.fysiksektionen.se/fysiksektionen/pl/{data['linked_english_post_id']}) |"

    return table

def handel_new_posted(driver: Driver, post):
    thread = driver.posts.get_thread(post["id"])
    for reply_post_id in thread["order"][::-1]:
        if reply_post_id == post["id"]:
            continue
        if '[]({"original_linked_post"' in thread["posts"][reply_post_id]["message"]:
            return

    data = {
            "english_info_has_been_sent": False,
            "time": None,
            "channel_id": None,
            "linked_english_post_id": None
            }

    table = create_data_table(driver, data)
    send_dm(driver, post["user_id"], f"""Hello, thank you for flying with us

{get_help_text()}

Current settings:
{get_current_settings(driver, data, table)}""", root_id = post["id"])

def get_current_settings(driver, data, table):
    send_not_send = "Missing some settings, will not send message."
    if data["channel_id"] is not None \
            and data["time"] is not None \
            and "<channel not found>" not in table \
            and "<invalid or missing channel id>" not in table:
        # Note (Elias): this will trigger if a channel is called <invalid or missing channel id> or <channel not found>. That will have to be fixed when the times comes. This minimizes the number of API calls.
        channel_name = get_channel_name(driver, data["channel_id"])
        mattermost_channel_link = f"https://mattermost.fysiksektionen.se/{get_channel_team_name(driver, data['channel_id'])}/channels/{get_channel_name(driver, data['channel_id'])}"
        send_not_send = f"Message will be sent in [~{channel_name}]({mattermost_channel_link}) at `{data['time']}`"

    return f"""
{table}
{send_not_send}
[]({json.dumps(data)})"""

def send_current_settings(driver, post, data):
    table = create_data_table(driver, data)

    will_send_english_info = False

    if data["channel_id"] is not None \
            and data["time"] is not None \
            and "<channel not found>" not in table \
            and "<invalid or missing channel id>" not in table:
        if not data["english_info_has_been_sent"]:
            will_send_english_info = True
            data["english_info_has_been_sent"] = True

    message = get_current_settings(driver, data, table)
    send_dm(driver, post["user_id"], message, root_id = post["root_id"])

    if will_send_english_info:
        send_dm(driver, post["user_id"], "Message configuration is finished. You can choose to send an english message as well using the `english`", root_id = post["root_id"])

    # TODO: save settings in static message database

def handle_reply(driver: Driver, post):
    replies = driver.posts.get_thread(post["root_id"])
    last_saved_data = None
    is_linked_message = False
    for reply_post_id in replies["order"][::-1]:
        if replies["posts"][reply_post_id]["user_id"] != driver.client.userid:
            continue

        lines = list(filter(None, replies["posts"][reply_post_id]["message"].split("\n")))
        if len(lines) == 0:
            continue

        last_line = lines[-1]
        if "[]({" not in last_line:
            continue

        data_part = last_line[3:-1] # remove '[](' and ')' from []({what we care about})
        last_saved_data = json.loads(data_part)
        print(last_saved_data)
        break

    if last_saved_data is None:
        send_dm(driver, post["user_id"], "Could not find any previous saved data - this should not happen. Please contact an admin for help.", root_id = post["root_id"])
        return

    if "original_linked_post" in last_saved_data:
        send_dm(driver, post["user_id"], "There is a linked english message, edit the settings of the original message to change time.", root_id = post["root_id"])
        return

    command = post["message"].strip()
    if command in CHANNEL_KEYWORDS:
        last_saved_data["channel_id"] = CHANNEL_KEYWORDS[command]
        send_current_settings(driver, post, last_saved_data)
    elif re.match(r"^[a-z0-9]{26}$", command): 
        try:
            channel = driver.channels.get_channel(command)
        except mattermostdriver.exceptions.ResourceNotFound:
            send_dm(driver, post["user_id"], "Invalid channel-id. Contact @ellundel or @eskilny if you need help.")
            return
        except mattermostdriver.exceptions.InvalidOrMissingParameters:
            send_dm(driver, post["user_id"], "Invalid formatted channel-id. Contact @ellundel or @eskilny if you need help.")
            return

        # TODO: verify that the user has write access to channel

        last_saved_data["channel_id"] = command
        send_current_settings(driver, post, last_saved_data)
    elif command == "english":
        if last_saved_data["linked_english_post_id"] is not None:
            send_dm(driver, post["user_id"], "There is already a linked english message.", root_id = post["root_id"])
            return

        # TODO: create translation
        eng_post = send_dm_as_other_user(driver, post["user_id"], driver.client.userid, """English translation""", root_id = None)

        original_post_data = {"original_linked_post": post["root_id"]}

        send_dm(driver, post["user_id"], f"""Linked to [original message](https://mattermost.fysiksektionen.se/fysiksektionen/pl/{post['root_id']}).
[]({json.dumps(original_post_data)})""",
                root_id = eng_post["id"])

        last_saved_data["linked_english_post_id"] = eng_post["id"]
        send_current_settings(driver, post, last_saved_data)
    elif re.match(r"^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-2]{1}[0-9]{1}:[0-5]{1}[0-9]{1}$", command):
        try:
            new_date = datetime.datetime.strptime(command, "%Y-%m-%d %H:%M")
        except ValueError:
            send_dm(driver, post["user_id"], "Invalid date format. Please use the format YYYY-MM-DD HH:MM.", root_id = post["root_id"])
            return

        if new_date < datetime.datetime.now():
            send_dm(driver, post["user_id"], "Date is in the past. Can only schedule in the future.", root_id = post["root_id"])
            return

        if new_date - datetime.datetime.now() > datetime.timedelta(days = 31):
            send_dm(driver, post["user_id"], "Date is too far in the future. Can only schedule one month in the future.", root_id = post["root_id"])
            return

        last_saved_data["time"] = command
        send_current_settings(driver, post, last_saved_data)
    else:
        send_dm(driver, post["user_id"], f"""Unknown command, contact @ellundel or @eskilny if you need help.
{get_help_text()}""", root_id = post["root_id"])

def handle_posted(driver: Driver, data):
    if data["channel_type"] != "D": # We only care about replies in DMs
        return

    post = json.loads(data["post"])

    if post["user_id"] == driver.client.userid:
        return

    if not post["root_id"]:
        handel_new_posted(driver, post)
    else:
        handle_reply(driver, post)

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

    print("Setup done. Listening for new posts...")

    ws.join()

if __name__ == "__main__":
    main()
