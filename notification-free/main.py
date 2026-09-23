from eliasmamo_import import *
import json
import logging
from queue import Empty, Queue

logger = logging.getLogger(__name__)

def get_admin_roles(driver: Driver):
    roles = {}
    for team in driver.teams.get_user_teams(driver.client.userid):
        members = driver.client.get(
            f'/users/{driver.client.userid}/teams/{team["id"]}/channels/members'
        )
        roles.update({member["channel_id"]: member["scheme_admin"] for member in members})
    return roles

def channel_member_updated(driver: Driver, data, admin_roles):
    channel_member = json.loads(data["channelMember"])
    if channel_member['user_id'] != driver.client.userid:
        return

    channel_id = channel_member["channel_id"]
    is_admin = channel_member["scheme_admin"]
    was_admin = admin_roles.get(channel_id, False)
    admin_roles[channel_id] = is_admin
    if is_admin == was_admin:
        return

    update = only_notify_mentions_for_channel if is_admin else full_notifications_for_channel
    users = get_all_channel_members(driver, channel_id)
    updated = failed = 0
    for user in users:
        if user["user_id"] == driver.client.userid:
            continue
        try:
            update(driver, channel_id=channel_id, user_id=user["user_id"])
            updated += 1
        except Exception:
            failed += 1
            logger.exception("Failed to update notifications: channel=%s user=%s", channel_id, user["user_id"])
    logger.info("Notification update: channel=%s admin=%s updated=%s failed=%s", channel_id, is_admin, updated, failed)

def new_user(driver: Driver, data):
    if data["channel_name"] == "town-square":
        return

    post = json.loads(data["post"])
    if post["type"] not in ("system_add_to_channel", "system_join_channel"):
        return

    user_id = post["props"]["addedUserId"] if post["type"] == "system_add_to_channel" else post["user_id"]
    if user_id == driver.client.userid:
        return

    me = driver.channels.get_channel_member(post["channel_id"], driver.client.userid)
    if not me["scheme_admin"]:
        return

    only_notify_mentions_for_channel(driver, post["channel_id"], user_id)

def process_events(driver: Driver, ws, events, admin_roles):
    while True:
        try:
            event, data = events.get(timeout=1)
        except Empty:
            if not ws.thread.is_alive():
                raise ConnectionError("Notification bot WebSocket disconnected")
            continue

        try:
            if event == "posted":
                new_user(driver, data)
            elif event == "channel_member_updated":
                channel_member_updated(driver, data, admin_roles)
        except Exception:
            logger.exception("Failed to handle event=%s", event)

def main():
    from secret import TOKEN

    logging.basicConfig(level=logging.INFO)
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

    admin_roles = get_admin_roles(driver)
    events = Queue()
    ws = WebSocket(TOKEN)

    ws.subscribe("posted", lambda data: events.put(("posted", data)))
    ws.subscribe("channel_member_updated", lambda data: events.put(("channel_member_updated", data)))

    logger.info("Setup done. Listening for membership changes...")
    process_events(driver, ws, events, admin_roles)

if __name__ == "__main__":
    main()
