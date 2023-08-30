from threading import Thread
import json

from eliasmamo_import import *
from secret import TOKEN
from configuration import *


def new_user(driver, data):
    add_to_default_channels(driver, data, TEAM_ID, CHANNELS)
    manage_channel_categories(driver, data["user_id"], TEAM_ID, CHANNELS, CATEGORIES)
    enable_all_notifications(driver, data["user_id"])
    driver.teams.add_user_to_team(TEAM_ID, {"team_id": TEAM_ID, "user_id": data["user_id"]})

def add_channel_members_to_users_in_channel(driver: Driver, channel, channel_id, users_in_channels):
    users_in_channels[channel] = set(get_channel_members(driver, channel_id))

def add_channel_member(driver: Driver, channel, user_id, users_in_channels):
    driver.channels.add_user(COURSE_CHANNELS[channel], {"user_id": user_id})
    users_in_channels[channel].add(user_id)

def remove_channel_member(driver: Driver, channel, user_id, users_in_channels):
    if user_id not in users_in_channels[channel]:
        return
    driver.channels.remove_channel_member(COURSE_CHANNELS[channel], user_id)
    users_in_channels[channel].remove(user_id)

class CourseChannels:
    # Note (Elias): Here are some thougts. Since the channels are open, people can join and leave specific channels if they please. For now I think it is best to not forcibly remove people other than when necessary. So when someone removes their reaction, they will be removed from the appropriate channels. But, if when the program starts, someone is in a channel that they do not have the reaction for, they will not be removed.
    # TODO: Will need to handle when the period changes, should people be removed? Or only added to the new ones?
    def __init__(self, driver: Driver):
        self.driver = driver

        self.users_in_channels = {}
        self.reactions = {}
        self.users_should_channels = {}

        self.setup_reactions_and_users_in_channels()
        self.build_user_should_channels()
        self.fix_diff()

        print("CourseChannels - done with init setup")

    def setup_reactions_and_users_in_channels(self):
        self.reactions = {}
        for reaction in (self.driver.reactions.get_reactions_of_post(post_id = REACTION_POST_ID) or []):
            if reaction["user_id"] not in self.reactions:
                self.reactions[reaction["user_id"]] = set()
            self.reactions[reaction["user_id"]].add(reaction["emoji_name"])

        self.users_in_channels = {}
        threads = []
        for channel in COURSE_CHANNELS:
            thread = Thread(target = add_channel_members_to_users_in_channel, args = (self.driver, channel, COURSE_CHANNELS[channel], self.users_in_channels))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def build_user_should_channels(self):
        self.users_should_channels = {}

        # Temporary hack
        f0_members = set(get_team_members(self.driver, "1ymsbdqk83dzmnx3e1ttgsbf7w"))
        fysiksektionen_members = set(get_team_members(self.driver, "71bh96izu7f1iee7ayhuan9itr"))
        mottagningen_members = set(get_team_members(self.driver, "b7hgwxzpzibdtdicycojcsn54w"))
        f0_users = f0_members - fysiksektionen_members - mottagningen_members

        for user in self.reactions:
            if user not in self.users_should_channels:
                self.users_should_channels[user] = set()

            if "triangular_ruler" in self.reactions[user] and "f0" in self.reactions[user] or user in f0_users:
                self.users_should_channels[user] |= CHANNEL_GROUPS["CTMAT-f0"]
            if "thermometer" in self.reactions[user] and "f0" in self.reactions[user] or user in f0_users:
                self.users_should_channels[user] |= CHANNEL_GROUPS["CTFYS-f0"]

    def fix_diff(self):
        threads = []
        modified_users = []
        for user in self.users_should_channels:
            if len(self.users_should_channels[user]) == 0:
                continue

            for channel in self.users_should_channels[user]:
                if user in self.users_in_channels[channel]:
                    continue
                print(f"Adding '{user}' to '{channel}'")
                thread = Thread(target = add_channel_member, args = (self.driver, channel, user, self.users_in_channels))
                thread.start()
                threads.append(thread)
                modified_users.append(user)

        for thread in threads:
            thread.join()

        threads = []
        for user in modified_users:
            thread = Thread(target = manage_channel_categories, args = (self.driver, user, TEAM_ID, CHANNELS, CATEGORIES))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def reaction_added(self, data):
        reaction = json.loads(data["reaction"])

        if reaction["post_id"] != REACTION_POST_ID:
            return

        if reaction["user_id"] not in self.reactions:
            self.reactions[reaction["user_id"]] = set()

        self.reactions[reaction["user_id"]].add(reaction["emoji_name"])

        self.build_user_should_channels()
        self.fix_diff()

    def reaction_removed(self, data):
        reaction = json.loads(data["reaction"])

        if reaction["post_id"] != REACTION_POST_ID:
            return

        if reaction["user_id"] not in self.reactions:
            self.reactions[reaction["user_id"]] = set()

        if reaction["emoji_name"] in self.reactions[reaction["user_id"]]:
            self.reactions[reaction["user_id"]].remove(reaction["emoji_name"])

        user_should_channels_before = self.users_should_channels[reaction["user_id"]]
        self.build_user_should_channels()

        for channel in [*(user_should_channels_before - self.users_should_channels[reaction["user_id"]])]:
            if reaction["user_id"] in self.users_in_channels[channel]:
                print(f"Removing '{reaction['user_id']}' from '{channel}'")
                remove_channel_member(self.driver, channel, reaction["user_id"], self.users_in_channels)

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
    cc = CourseChannels(driver)

    print("Listening for new users")
    ws.subscribe("user_added", lambda data: new_user(driver, data))
    ws.subscribe("reaction_added", cc.reaction_added)
    ws.subscribe("reaction_removed", cc.reaction_removed)

    delete_new_posts_in_clean_channels(driver, CHANNELS)

    #for ch in driver.channels.get_public_channels(TEAM_ID):
    #    print(f'"{ch["name"]}": "{ch["id"]}",')

    if False:
        print("Adding new users to default channels...")
        for user in get_team_members(driver, TEAM_ID):
            new_user(driver, {"user_id": user, "team_id": TEAM_ID})
        print("Adding new users to default channels ... Done")

    ws.join()

    # User addad to team -> Add to channel {'event': 'user_added', 'data': {'team_id': 'g16tqepa3ffntkfnnwqyapkzkr', 'user_id': 'zu7i4ow3obfa3egwpau59r6s4a'}, 'broadcast': {'omit_users': None, 'user_id': '', 'channel_id': '8e9yhhagtjbnpdyr6eiox8i3oa', 'team_id': '', 'connection_id': ''}, 'seq': 8}

if __name__ == "__main__":
    main()
