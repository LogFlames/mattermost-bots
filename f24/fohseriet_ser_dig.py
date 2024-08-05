from eliasmamo_import import *
from secret import TOKEN
import json
import time
from threading import Thread

FOHSARE = ("yfoh44x7ap893d95q7h4i5t9dr", "6tkf3ofjpbywtksumh6xwn61pr", "8hrwhomdtty1tg4inr6rwxjo1w")

def clean_fohsare(driver: Driver, data):
    reaction = json.loads(data["reaction"])
    if reaction["emoji_name"] == "fohserietserdig" and \
        reaction["user_id"] not in FOHSARE:
        driver.reactions.delete_reaction(reaction["user_id"], reaction["post_id"], "fohserietserdig")

def clean_message(driver: Driver, data):
    post = json.loads(data["post"])
    if ":fohserietserdig:" in post["message"] and \
        post["user_id"] not in FOHSARE:
        new_message = post["message"].replace(":fohserietserdig:", ":eyes:")
        driver.posts.update_post(post["id"], { "id": post["id"], "message": new_message })

def update_user_status(driver: Driver):
    while True:
        for fohsare in FOHSARE:
            driver.status.update_user_status(fohsare, {"user_id": fohsare, "status": "online"})
        time.sleep(30)

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

    ws.subscribe("reaction_added", lambda data: clean_fohsare(driver, data))
    ws.subscribe("posted", lambda data: clean_message(driver, data))
    ws.subscribe("post_edited", lambda data: clean_message(driver, data))

    always_online_thread = Thread(target = lambda: update_user_status(driver))
    always_online_thread.start()


    if True:
        for post in driver.posts.get_posts_for_channel("nhdqa8hkcfdrfqfmew1q5r5xne")["posts"]:
            print(f"Checking message: {post}")
            for reaction in (driver.reactions.get_reactions_of_post(post) or []):
                clean_fohsare(driver, {"reaction": json.dumps({"user_id": reaction["user_id"], "post_id": post, "emoji_name": reaction["emoji_name"]})})

    always_online_thread.join()
    ws.join()

if __name__ == "__main__":
    main()
