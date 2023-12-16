from eliasmamo_import import *
from secret import TOKEN
from configuration import *
import json
from tqdm import tqdm

def fix_users(driver):
    print("Fixing new users default channels...")
    users = get_team_members(driver, TEAM_ID)
    reactions = driver.reactions.get_reactions_of_post(MESSAGE_WITH_ENGLISH_REACTIONS_POST_ID)

    print("Getting reactions...")
    user_in_english = {user: False for user in users}
    for reaction in reactions:
        if reaction["post_id"] == MESSAGE_WITH_ENGLISH_REACTIONS_POST_ID and reaction["emoji_name"] in ("english", "en_english"):
            user_in_english[reaction["user_id"]] = True

    print("Getting reactions... Done")
    for user_id in tqdm(users):
        channels_to_add_to = {channel: CHANNELS[channel] for channel in DEFAULT_CHANNELS}

        if user_in_english[user_id]:
            channels_to_add_to |= {channel: CHANNELS[channel] for channel in ENGLISH_CHANNELS}

        add_to_default_channels(driver, {"user_id": user_id, "team_id": TEAM_ID}, TEAM_ID, channels_to_add_to)

        manage_channel_categories(driver, user_id, TEAM_ID, CHANNELS, CATEGORIES)
        enable_all_notifications(driver, user_id)
    print("Fixing new users default channels ... Done")


def new_user(driver, data):
    channels_to_add_to = {channel: CHANNELS[channel] for channel in DEFAULT_CHANNELS}

    add_to_default_channels(driver, data, TEAM_ID, channels_to_add_to)

    manage_channel_categories(driver, data["user_id"], TEAM_ID, CHANNELS, CATEGORIES)
    enable_all_notifications(driver, data["user_id"])

def add_to_english(driver, user_id):
    channels_to_add_to = {channel: CHANNELS[channel] for channel in ENGLISH_CHANNELS}

    add_to_default_channels(driver, {"user_id": user_id, "team_id": TEAM_ID}, TEAM_ID, channels_to_add_to)

    manage_channel_categories(driver, user_id, TEAM_ID, CHANNELS, CATEGORIES)

def reacted(driver, data):
    reaction = json.loads(data["reaction"])

    if reaction["post_id"] == MESSAGE_WITH_ENGLISH_REACTIONS_POST_ID:
        if reaction["emoji_name"] in ("english", "en_english", "en"):
            add_to_english(driver, reaction["user_id"])

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

    print("Listening for new users")
    ws.subscribe("user_added", lambda data: new_user(driver, data))
    ws.subscribe("reaction_added", lambda data: reacted(driver, data))

    delete_new_posts_in_clean_channels(driver, CHANNELS)

    if False:
        fix_users(driver)

    ws.join()

    # User addad to team -> Add to channel {'event': 'user_added', 'data': {'team_id': 'g16tqepa3ffntkfnnwqyapkzkr', 'user_id': 'zu7i4ow3obfa3egwpau59r6s4a'}, 'broadcast': {'omit_users': None, 'user_id': '', 'channel_id': '8e9yhhagtjbnpdyr6eiox8i3oa', 'team_id': '', 'connection_id': ''}, 'seq': 8}

if __name__ == "__main__":
    main()
