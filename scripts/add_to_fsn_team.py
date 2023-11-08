from eliasmamo_import import *
from secret import TOKEN

FSN_TEAM = "419spm3ugf8axc8chupqw9e5bo"

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

    fsn_members = get_team_members(driver, FSN_TEAM)

    for team in driver.teams.get_teams({"per_page": 100}):
        for user in get_team_members(driver, team["id"]):
            if user not in fsn_members:
                print(f"Adding user {user} to FSN from team {team['name']}")
                driver.teams.add_user_to_team(FSN_TEAM, {"team_id": FSN_TEAM, "user_id": user})
                fsn_members.append(user)

    #for user in driver.teams.get_team_members(TEAM_ID, {"per_page": 2000}):
    #    manage_channel_categories(driver, user["user_id"], TEAM_ID)

    # User addad to team -> Add to channel {'event': 'user_added', 'data': {'team_id': 'g16tqepa3ffntkfnnwqyapkzkr', 'user_id': 'zu7i4ow3obfa3egwpau59r6s4a'}, 'broadcast': {'omit_users': None, 'user_id': '', 'channel_id': '8e9yhhagtjbnpdyr6eiox8i3oa', 'team_id': '', 'connection_id': ''}, 'seq': 8}

if __name__ == "__main__":
    main()
