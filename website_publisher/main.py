from eliasmamo_import import *
from secret import TOKEN
from publish import create_wp_post, update_wp_post, upload_wp_image
from configuration import AUTHENTICATED_USERS, POSTABLE_CHANNELS, EMOJI_MAP, LANG, NAMND_EMAIL_MAP, NAMND_FORMATTED_NAME, NAMND_FORMATTED_NAME_EN
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

def transform_mattermost_message_to_website_html(driver, message, namnd, lang, files_to_include):
    formatted_name = NAMND_FORMATTED_NAME_EN[namnd] if lang == "en" else NAMND_FORMATTED_NAME[namnd]
    responsible = "Responsible Committee" if lang == "en" else "Ansvarig nämnd"
    ansvarig_namnd = f"<h6>{responsible}: <a href=\"mailto:{NAMND_EMAIL_MAP[namnd]}\">{formatted_name}</a></h6>"

    files = []
    for file in files_to_include:
        files.append(f'<img class="size-medium wp-image-{file["id"]} aligncenter" src="{file["guid"]}" alt="Auto-uploaded post attachment image" width="50%" />')

    return convert_markdown(
            html_escape_codes(
                replace_usertags(
                    driver, 
                    remove_emojis(
                        message + "\n" +
                        "\n".join(files) + "\n" + 
                        ansvarig_namnd
                        )
                    )
                )
            )


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

    reactions_on_post = driver.reactions.get_reactions_of_post(reaction["post_id"])

    for reaction_on_post in reactions_on_post:
        if reaction_on_post["user_id"] == driver.client.userid:
            return

    namnd = EMOJI_MAP[reaction["emoji_name"]]

    if reaction["user_id"] not in AUTHENTICATED_USERS[namnd]:
        send_dm(driver, reaction["user_id"], f"You lack permission to create posts on the website for `{namnd}`. Please contact Mattermästare at mattermost@f.kth.se if you think this is a mistake.")
        print(f"{reaction['user_id']} attempted to react with {reaction['emoji_name']} but is not authenticated. Sent DM.")
        return

    if reaction["channel_id"] not in POSTABLE_CHANNELS:
        send_dm(driver, reaction["user_id"], "Messages in this channel cannot be posted to the website. If you think this is a mistake please contact Mattermästare at mattermost@f.kth.se.")
        print(f"{reaction['user_id']} attempted to react with {reaction['emoji_name']} in an non-postable channel. Sent DM.")
        return

    driver.reactions.create_reaction({"post_id": reaction["post_id"], "emoji_name": reaction["emoji_name"], "user_id": driver.client.userid})

    post = driver.posts.get_post(reaction["post_id"])

    if not post["message"]:
        return

    files_to_include = []
    if "metadata" in post and "files" in post["metadata"] and len(post["metadata"]["files"]) > 0:
        for file in post["metadata"]["files"]:
            if "mime_type" not in file or not file["mime_type"].startswith("image/"):
                continue

            try: 
                image = driver.files.get_file(file["id"])
                res_status, res = upload_wp_image(namnd, image.content, file["name"])
                if res_status >= 400:
                    print(f"Failed to upload {file['name']} with id: {file['id']}")
                    continue

                if "guid" in res and "rendered" in res["guid"]:
                    print(f"Uploaded image {file['name']} with id: {file['id']}, got guid: {res['guid']['rendered']}")
                    files_to_include.append({"guid": res["guid"]["rendered"], "id": res["id"]})
                else:
                    print(f"Failed to upload {file['name']} with id: {file['id']}, no guid in response")
            except Exception as e:
                print(f"Failed to upload {file['name']} with id: {file['id']}, exception: {e}")

    lines = list(filter(None, post["message"].split("\n")))
    
    if len(lines) == 0:
        title = ""
    else:
        title = html_escape_codes(remove_emojis(lines[0]))

    lang = LANG[POSTABLE_CHANNELS[post["channel_id"]]]

    message = transform_mattermost_message_to_website_html(driver, post["message"], namnd, lang, files_to_include)

    res_status, res = create_wp_post(namnd = namnd, title = title, message = message, timestamp = post["create_at"] / 1000, lang = lang, status = "draft")

    if res_status >= 400:
        print("Got non-ok status from f.kth.se")
        print(res)
        send_dm(driver, reaction["user_id"], f"An error occured while trying to create post on the website. Please check with Mattermästare at mattermost@f.kth.se.")
        return

    wp_post_id = res["id"]
    mattermost_message_link = f"https://mattermost.fysiksektionen.se/{CHANNEL_ID_TO_TEAM_URL[post['channel_id']]}/pl/{reaction['post_id']}"

    data = json.dumps({"wp_post_id": wp_post_id, "post_id": reaction["post_id"], "namnd": namnd, "files": files_to_include}, separators=(",", ":"))

    print(f"Sent to {post['user_id']}: Publish post message with links to {mattermost_message_link} and {res['link']}")
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

    if post["user_id"] == driver.client.userid:
        return

    if not post["root_id"]:
        send_dm(driver, post["user_id"], "Titles should be written as a reply in the thread of the message.")
        print(f"{post['user_id']} sent a direct DM, answered that titles should be written in a thread.")
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

    files_to_include = []
    if "files" in publish_data:
        files_to_include = publish_data["files"]
    lang = LANG[POSTABLE_CHANNELS[publish_content_post["channel_id"]]]
    content = transform_mattermost_message_to_website_html(driver, publish_content_post["message"], namnd, lang, files_to_include)
    title = html_escape_codes(remove_emojis(post["message"]))

    res_status, res = update_wp_post(namnd, publish_data["wp_post_id"], title = title, message = content, status = "publish")

    if res_status >= 400:
        print("Got non-ok status from f.kth.se")
        print(res)
        driver.posts.create_post({"channel_id": post["channel_id"], "message": f"An error occured while trying to update the post on the website. Please check with Mattermästare at mattermost@f.kth.se.", "root_id": post["root_id"]})
        return

    print(f"Sent to {post['user_id']}: Published and/or updated post on website with new title and content. With WP post id: {publish_data['wp_post_id']}")
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

    print("Setup done. Listening for new posts and reactions...")

    ws.join()

if __name__ == "__main__":
    main()
