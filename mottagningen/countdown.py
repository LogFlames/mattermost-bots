from eliasmamo_import import *
from secret import TOKEN
from datetime import datetime
import math

COUNTDOWN_CHANNEL = "uduyxpg5stgttfkiehqwszf7he"

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

    diff = (datetime.fromisoformat("2024-08-12T00:00:00.000000") - datetime.today())
    dagar = diff.days + 1

    driver.channels.update_channel(COUNTDOWN_CHANNEL, {"id": COUNTDOWN_CHANNEL, "name": "countdown", "display_name": f"{dagar} dag{'ar' if dagar != 1 else ''} kvar till dag Ø"})

    posts = driver.posts.get_posts_for_channel(COUNTDOWN_CHANNEL)["posts"]
    for post_id in posts:
        if posts[post_id]["type"] == "system_displayname_change":
            driver.posts.delete_post(post_id)

    driver.posts.create_post({"channel_id": COUNTDOWN_CHANNEL, "message": f"@mottagningen24 {dagar} dag{'ar' if dagar != 1 else ''} kvar till dag Ø"})

if __name__ == "__main__":
    main()
