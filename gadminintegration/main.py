from eliasmamo_import import *
from configuration import NAMNDER
from gint import get_group_members
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
#    ws = WebSocket(TOKEN)
#    ws.join()

    print("Loading all users...")
    USERS = {}
    for user in get_all_users(driver):
        USERS[user["username"]] = user["id"]
    print("Loading all users... Done")


    print("Loading all teams...")
    page = 0
    TEAMS = {}
    while True:
        new_teams = driver.teams.get_teams({"page": page, "per_page": 60})
        page += 1

        if new_teams:
            for team in new_teams:
                TEAMS[team["name"]] = team["id"]
        else:
            break
    print("Loading all teams... Done")


    print("Checking all team-names...")
    for namnd in NAMNDER:
        for team in namnd["teams"]:
            if team not in TEAMS:
                print(f"Team {team} not in TEAMS from MaMo. Check spelling.")
                return
    print("Checking all team-names... Done")

    print("Adding all GAdmin members to teams...")
    for namnd in NAMNDER:
        print(f"Processing {namnd}...")
        members = set()
        for group in namnd["groups"]:
            print(f"    Getting {group}...")
            members |= get_group_members(group = group, recursive = True, include_subgroups = False)
            print(f"    Getting {group}... Done")

        members = set(map(lambda x: x.replace("@fysiksektionen.se", ""), members))

        for team in namnd["teams"]:
            team_members = set(get_team_members(driver, team_id = TEAMS[team]))

            for member in members:
                if member not in USERS:
                    continue

                if USERS[member] in team_members:
                    continue

                print(f"Adding {member} ({USERS[member]}) to {team}")
                driver.teams.add_user_to_team(team_id = TEAMS[team], options = {"team_id": TEAMS[team], "user_id": USERS[member]})
    print("Adding all GAdmin members to teams... Done")


if __name__ == "__main__":
    main()
