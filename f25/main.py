from eliasmamo_import import *
from secret import TOKEN
from configuration import *

def new_user(driver, data):
    add_to_default_channels(driver, data, TEAM_ID, CHANNELS)
    manage_channel_categories(driver, data["user_id"], TEAM_ID, {**CHANNELS, **HIDDEN_CHANNELS}, CATEGORIES)
    enable_all_notifications(driver, data["user_id"])

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

    if True:
        print("Adding new users to default channels...")
        team_members = get_team_members(driver, TEAM_ID)
        for i, user in enumerate(team_members):
            print(f"Handling user: {user} {i + 1}/{len(team_members)}")
            new_user(driver, {"user_id": user, "team_id": TEAM_ID})
        print("Adding new users to default channels ... Done")

    ws.join()

if __name__ == "__main__":
    main()
