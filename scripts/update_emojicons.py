from eliasmamo_import import *
from secret import TOKEN

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

    users = get_all_users(driver)

    for user in users:
        driver.preferences.save_user_preferences(user["id"], [{"user_id": user["id"], "category": "display_settings", "name": "render_emoticons_as_emoji", "value": "false"}])

if __name__ == "__main__":
    main()
