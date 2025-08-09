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

    TEAM_ID = "b7hgwxzpzibdtdicycojcsn54w" # Mottagningen

    members = get_team_members(driver, TEAM_ID)

    CHANNEL_ID = "3uoht86my7r5znzi819iyqc9to" # Frågelådan

    driver.channels.add_user(CHANNEL_ID, {"user_ids": members})

if __name__ == "__main__":
    main()
