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

    teams = driver.teams.get_user_teams(driver.client.userid)
    for team in teams:
        channels = driver.channels.get_channels_for_user(driver.client.userid, team["id"])
        for channel in channels:
            user = driver.channels.get_channel_member(channel["id"], driver.client.userid)
            print(f"{team['display_name']}: {channel['display_name']} (is admin: {'channel_admin' in user['roles']})")

if __name__ == "__main__":
    main()
