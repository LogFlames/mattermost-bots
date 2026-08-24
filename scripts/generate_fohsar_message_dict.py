# Expected input format (one post per line):
# https://mattermost.fysiksektionen.se/fysiksektionen/pl/<post_id>
# <post_id>

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from mattermostdriver import Driver

from secret import TOKEN


POST_ID_PATTERN = re.compile(r"^[a-z0-9]{26}$")


def read_post_ids(path):
    post_ids = []

    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        value = line.strip()
        if not value:
            continue

        post_id = urlparse(value).path.rstrip("/").rsplit("/", 1)[-1]
        if not POST_ID_PATTERN.fullmatch(post_id):
            raise ValueError(f"Invalid post ID on line {line_number}: {value}")

        post_ids.append(post_id)

    return post_ids


def get_messages_by_username(driver, post_ids):
    messages_by_username = {}
    usernames_by_user_id = {}

    for post_id in post_ids:
        post = driver.posts.get_post(post_id)
        user_id = post["user_id"]

        if user_id not in usernames_by_user_id:
            user = driver.users.get_user(user_id)
            usernames_by_user_id[user_id] = user["username"]

        username = usernames_by_user_id[user_id]
        messages_by_username.setdefault(username, []).append(post_id)

    return messages_by_username


def format_messages_by_username(messages_by_username):
    lines = ["blacklisted_messages_2026 = {"]
    entries = list(messages_by_username.items())

    for index, (username, post_ids) in enumerate(entries):
        comma = "," if index < len(entries) - 1 else ""
        lines.append(f"        {json.dumps(username)}: {json.dumps(post_ids)}{comma}")

    lines.append("        }")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Group Mattermost post IDs by the username that created each post."
    )
    parser.add_argument(
        "--in",
        dest="input_path",
        type=Path,
        required=True,
        help="file containing post IDs or links",
    )
    args = parser.parse_args()

    driver = Driver(
        {
            "url": "mattermost.fysiksektionen.se",
            "basepath": "/api/v4",
            "verify": True,
            "scheme": "https",
            "port": 443,
            "auth": None,
            "token": TOKEN,
            "keepalive": True,
            "keepalive_delay": 5,
        }
    )
    driver.login()

    messages_by_username = get_messages_by_username(
        driver, read_post_ids(args.input_path)
    )
    print(format_messages_by_username(messages_by_username))


if __name__ == "__main__":
    main()
