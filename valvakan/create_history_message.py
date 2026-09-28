from mattermostdriver import Driver

from configuration import HISTORY_CHANNEL_ID
from secret import TOKEN


def main():
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
    post = driver.posts.create_post({"channel_id": HISTORY_CHANNEL_ID, "message": "```\nHistory is empty.\n```"})
    print(post["id"])


if __name__ == "__main__":
    main()