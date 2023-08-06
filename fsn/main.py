from eliasmamo_import import *
from secret import TOKEN
from configuration import *

FSN_TEAM = "419spm3ugf8axc8chupqw9e5bo"

def new_user(driver, data):
    add_to_default_channels(driver, data, TEAM_ID, CHANNELS)
    manage_channel_categories(driver, data["user_id"], TEAM_ID, CHANNELS, CATEGORIES)
    enable_all_notifications(driver, data["user_id"])
    driver.teams.add_user_to_team(FSN_TEAM, {"team_id": FSN_TEAM, "user_id": data["user_id"]})

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

    delete_new_posts_in_clean_channels(driver, CHANNELS)

    if False:
        print("Adding new users to default channels...")
        for user in get_team_members(driver, TEAM_ID):
            new_user(driver, {"user_id": user, "team_id": TEAM_ID})
        print("Adding new users to default channels ... Done")

    # User addad to team -> Add to channel {'event': 'user_added', 'data': {'team_id': 'g16tqepa3ffntkfnnwqyapkzkr', 'user_id': 'zu7i4ow3obfa3egwpau59r6s4a'}, 'broadcast': {'omit_users': None, 'user_id': '', 'channel_id': '8e9yhhagtjbnpdyr6eiox8i3oa', 'team_id': '', 'connection_id': ''}, 'seq': 8}

if __name__ == "__main__":
    main()
