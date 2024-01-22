from eliasmamo_import import *
from secret import TOKEN
from publish import create_wp_post, update_wp_post
from configuration import AUTHENTICATED_USERS, POSTABLE_CHANNELS, EMOJI_MAP
import json
import markdown
import re

def replace_usertags(driver: Driver, text):
    if "@" not in text:
        return text

    users = get_all_users(driver)

    for user in users:
        if "is_bot" in user and user["is_bot"]:
            continue
        reg = fr"@{re.escape(user['username'])}(?=[-_\.]*[^A-Za-z0-9-\._])"
        text = re.sub(reg, f"[@{user['first_name']} {user['last_name']}](mailto:{user['username']}@fysiksektionen.se)", text)

    return text

def convert_markdown(text):
    return markdown.markdown(text)

def html_escape_codes(text):
    return text.encode("latin1", "xmlcharrefreplace").decode("latin1")


def remove_emojis(text):
    return re.sub(r":[a-zA-Z0-9-_+]+:", "", text)

def get_teams_name(driver: Driver):
    channel_id_to_team_urls = {}
    for channel_id in POSTABLE_CHANNELS:
        channel = driver.channels.get_channel(channel_id)

        team = driver.teams.get_team(channel["team_id"])

        channel_id_to_team_urls[channel_id] = team["name"]

    return channel_id_to_team_urls

def handle_reaction_added(driver: Driver, data, CHANNEL_ID_TO_TEAM_URL):
    reaction = json.loads(data["reaction"])

    if reaction["user_id"] == driver.client.userid:
        return

    if reaction["emoji_name"] not in EMOJI_MAP:
        return 

    namnd = EMOJI_MAP[reaction["emoji_name"]]

    if reaction["user_id"] not in AUTHENTICATED_USERS[namnd]:
        send_dm(driver, reaction["user_id"], f"You lack permission to create posts on the website for `{namnd}`. Please contact Mattermästare at mattermost@f.kth.se if you think this is a mistake.")
        return

    if reaction["channel_id"] not in POSTABLE_CHANNELS:
        send_dm(driver, reaction["user_id"], "Messages in this channel cannot be posted to the website. If you think this is a mistake please contact Mattermästare at mattermost@f.kth.se.")
        return

    reactions_on_post = driver.reactions.get_reactions_of_post(reaction["post_id"])

    for reaction_on_post in reactions_on_post:
        if reaction_on_post["user_id"] == driver.client.userid:
            return

    driver.reactions.create_reaction({"post_id": reaction["post_id"], "emoji_name": reaction["emoji_name"], "user_id": driver.client.userid})

    post = driver.posts.get_post(reaction["post_id"])

    if not post["message"]:
        return

    lines = list(filter(None, post["message"].split("\n")))
    
    if len(lines) == 0:
        title = ""
    else:
        title = html_escape_codes(remove_emojis(lines[0]))

    message = convert_markdown(html_escape_codes(replace_usertags(driver, remove_emojis(post["message"]))))

    res_status, res = create_wp_post(namnd = namnd, title = title, message = message, timestamp = post["create_at"] / 1000, status = "draft")

    if res_status >= 400:
        print("Got non-ok status from f.kth.se")
        print(res)
        send_dm(driver, reaction["user_id"], f"An error occured while trying to create post on the website. Please check with Mattermästare at mattermost@f.kth.se.")
        return

    wp_post_id = res["id"]
    mattermost_message_link = f"https://mattermost.fysiksektionen.se/{CHANNEL_ID_TO_TEAM_URL[post['channel_id']]}/pl/{reaction['post_id']}"

    data = json.dumps({"wp_post_id": wp_post_id, "post_id": reaction["post_id"], "namnd": namnd}, separators=(",", ":"))

    send_dm(driver, reaction["user_id"], 
    f"""### Publish post to website
[Mattermost Message]({mattermost_message_link})
[Post on f.kth.se]({res["link"]})

**Please reply to this message with a title for the post on the website.** If you wish to change the title or update the content (in case the mattermost message has been edited) please reply with another (or the same) title again and the post on the website will be updated.

[-data-]({data})
""")

def handle_posted(driver: Driver, data):
    if data["channel_type"] != "D": # We only care about replies in DMs
        return

    post = json.loads(data["post"])

    if not post["root_id"]:
        return

    if post["user_id"] == driver.client.userid:
        return

    root_post = driver.posts.get_post(post["root_id"])

    lines = list(filter(None, root_post["message"].split("\n")))

    if len(lines) == 0:
        return

    last_line = lines[-1]

    if "[-data-]" not in last_line:
        return

    publish_data_message = last_line[9:-1] # remove '[-data-](' and ')' from [-data-]({what we care about})

    publish_data = json.loads(publish_data_message)

    namnd = publish_data["namnd"]

    if post["user_id"] not in AUTHENTICATED_USERS[namnd]:
        send_dm(driver, post["user_id"], f"You lack permission to create posts on the website for `{namnd}`. Please contact Mattermästare at mattermost@f.kth.se if you think this is a mistake.")
        return

    try:
        publish_content_post = driver.posts.get_post(publish_data["post_id"])
    except mattermostdriver.exceptions.ResourceNotFound:
        driver.posts.create_post({"channel_id": post["channel_id"], "message": "The original mattermost post seems to have been deleted, cannot get the post.", "root_id": post["root_id"]})
        return

    content = convert_markdown(html_escape_codes(replace_usertags(driver, remove_emojis(publish_content_post["message"]))))
    title = html_escape_codes(remove_emojis(post["message"]))

    res_status, res = update_wp_post(namnd, publish_data["wp_post_id"], title = title, message = content, status = "publish")

    if res_status >= 400:
        print("Got non-ok status from f.kth.se")
        print(res)
        driver.posts.create_post({"channel_id": post["channel_id"], "message": f"An error occured while trying to update the post on the website. Please check with Mattermästare at mattermost@f.kth.se.", "root_id": post["root_id"]})
        return

    driver.posts.create_post({"channel_id": post["channel_id"], "message": "Published and/or updated post on website with new title and content.", "root_id": post["root_id"]})

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

    CHANNEL_ID_TO_TEAM_URL = get_teams_name(driver)

    ws = WebSocket(TOKEN)

    ws.subscribe("reaction_added", lambda data: handle_reaction_added(driver, data, CHANNEL_ID_TO_TEAM_URL))
    ws.subscribe("posted", lambda data: handle_posted(driver, data))

    print("Setup done. Listening for new posts...")

    ws.join()

if __name__ == "__main__":
    main()
