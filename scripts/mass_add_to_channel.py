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

    CHANNEL_ID = "fwqdcizefb8j7b3edfs4znpkey"

    ch = driver.channels.get_channel(CHANNEL_ID)
    TEAM_ID = ch["team_id"]

    members = get_team_members(driver, TEAM_ID)

    driver.channels.add_user(CHANNEL_ID, {"user_ids": members})

if __name__ == "__main__":
    main()
