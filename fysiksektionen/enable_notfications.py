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

    users = set()
    for team in driver.teams.get_teams({"per_page": 100}):
        for user in get_team_members(driver, team["id"]):
            users.add(user)

    print(f"Found {len(users)} users, enabling notifications.")
    for user in users:
        print(f"Enabling notifications for: {user}")
        enable_all_notifications(driver, user)

    #for user in driver.teams.get_team_members(TEAM_ID, {"per_page": 2000}):
    #    manage_channel_categories(driver, user["user_id"], TEAM_ID)

    # User addad to team -> Add to channel {'event': 'user_added', 'data': {'team_id': 'g16tqepa3ffntkfnnwqyapkzkr', 'user_id': 'zu7i4ow3obfa3egwpau59r6s4a'}, 'broadcast': {'omit_users': None, 'user_id': '', 'channel_id': '8e9yhhagtjbnpdyr6eiox8i3oa', 'team_id': '', 'connection_id': ''}, 'seq': 8}

if __name__ == "__main__":
    main()
