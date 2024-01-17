from eliasmamo_import import *
from secret import TOKEN
from publish import create_post
from configuration import AUTHENTICATED_USERS, POSTABLE_CHANNELS, EMOJI_MAP
import json
import markdown


def get_markdown_title(message):
    for line in message.split("\n")[:5]:
        if line.startswith("#"):
            return line.lstrip("#").strip()

    return None

def handle_reaction(driver: Driver, data):
    reaction = json.loads(data["reaction"])
    if reaction["emoji_name"] not in EMOJI_MAP:
        return 

    if reaction["channel_id"] not in POSTABLE_CHANNELS:
        return

    if reaction["user_id"] == driver.client.userid:
        return

    namnd = EMOJI_MAP[reaction["emoji_name"]]

    if reaction["user_id"] not in AUTHENTICATED_USERS[namnd]:
        dm_channel = driver.channels.create_direct_message_channel([reaction["user_id"], driver.client.userid])
        driver.posts.create_post({
            "channel_id": dm_channel["id"], 
            "message": f"You lack permission to create posts on the website for {namnd}. Please contact webmaster at webmaster@f.kth.se if you think this is a mistake."})
        return

    reactions_on_post = driver.reactions.get_reactions_of_post(reaction["post_id"])

    for reaction_on_post in reactions_on_post:
        if reaction_on_post["user_id"] == driver.client.userid:
            return

    post = driver.posts.get_post(reaction["post_id"])

    if not post["message"]:
        return

    title = get_markdown_title(post["message"])

    if title is None:
        dm_channel = driver.channels.create_direct_message_channel([reaction["user_id"], driver.client.userid])
        driver.posts.create_post({
            "channel_id": dm_channel["id"], 
            "message": f"""### Saknar titel
Du försökte lägga upp ett meddelande som inlägg på f.kth.se. För att kunna göra detta behöver meddelandet innehålla en titel. Vänligen redigera meddelandet och lägg in en kort beskrivande titel och reagera igen för att lägga upp på hemsidan. En titel läggs till genom ett eller flera '#' i början av första raden. Se [Mattermost Dokumentation](https://docs.mattermost.com/collaborate/format-messages.html) för mer information kring formaterandet av meddelanden.
```
### Beskrivande titel till ditt meddelande
[Resten av meddelandet ...]
```"""})
        return

    driver.reactions.create_reaction({"post_id": reaction["post_id"], "emoji_name": reaction["emoji_name"], "user_id": driver.client.userid})

    create_post(namnd = namnd, title = title, message = markdown.markdown(post["message"]), status = "publish")

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

    ws.subscribe("reaction_added", lambda data: handle_reaction(driver, data))

    print("Setup done. Listening for new posts...")

    ws.join()

if __name__ == "__main__":
    main()
