from eliasmamo_import import *
from messages_swe import MESSAGES_SWE
from messages_eng import MESSAGES_ENG
from secret import TOKEN

INFO_CHANNEL_SWE = "dz1jak398fyhir1uxpya7grify"
INFO_CHANNEL_ENG = "1kfcce1i7py4ip1933fkb95jrh"

def send_to_channel(driver: Driver, CHANNEL, MESSAGES):

    old_posts = driver.posts.get_posts_for_channel(CHANNEL)

    for post in old_posts["posts"]:
        if old_posts["posts"][post]["user_id"] == driver.client.userid and \
                old_posts["posts"][post]["root_id"] == "":
            driver.posts.delete_post(old_posts["posts"][post]["id"])

    for mes in MESSAGES:
        ret = driver.posts.create_post({"channel_id": CHANNEL, "message": mes[0]})
        for reply in mes[1:]:
            driver.posts.create_post({"channel_id": CHANNEL, "message": reply, "root_id": ret["id"]})

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

    send_to_channel(driver, INFO_CHANNEL_SWE, MESSAGES_SWE)
    send_to_channel(driver, INFO_CHANNEL_ENG, MESSAGES_ENG)

if __name__ == "__main__":
    main()
