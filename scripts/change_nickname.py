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

    user_id = input("UserID: ")
    nickname = input("Nickname: ")

    user_props = driver.client.put(
            '/users/' + user_id + "/patch")

    user_props["nickname"] = nickname

    driver.client.put(
        '/users/' + user_id + '/patch',
        options = user_props
    )

    print(f"Updated {user_id}'s position to: {nickname}")

    #for user in driver.teams.get_team_members(TEAM_ID, {"per_page": 2000}):
    #    manage_channel_categories(driver, user["user_id"], TEAM_ID)

    # User addad to team -> Add to channel {'event': 'user_added', 'data': {'team_id': 'g16tqepa3ffntkfnnwqyapkzkr', 'user_id': 'zu7i4ow3obfa3egwpau59r6s4a'}, 'broadcast': {'omit_users': None, 'user_id': '', 'channel_id': '8e9yhhagtjbnpdyr6eiox8i3oa', 'team_id': '', 'connection_id': ''}, 'seq': 8}

if __name__ == "__main__":
    main()
