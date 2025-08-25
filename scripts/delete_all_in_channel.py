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

    channel_id = input("Channel ID of channel to clear of messages: ")

    for post in driver.posts.get_posts_for_channel(channel_id)["posts"]:
        driver.posts.delete_post(post)

if __name__ == "__main__":
    main()
