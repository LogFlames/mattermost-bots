from eliasmamo_import import *
from secret import TOKEN
import json
import time
from threading import Thread

FOHSARE = ("nwdqsc3ifjbybrxppxxdsf6d9w", "mqo9aogurbn75x4sjk53soiwzc", "snbz4s3zt3b6tezxm1mz77uwor", "fixxox8xyjb9dm8cffikeitgew")

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

    thread = Thread(target = lambda: update_user_status(driver))
    thread.start()


    if False:
        for post in driver.posts.get_posts_for_channel("1s5puiy3wby79pn94wf8ystepo")["posts"]:
            print(f"Checking message: {post}")
            for reaction in driver.reactions.get_reactions_of_post(post):
                clean_fohsare(driver, {"reaction": json.dumps({"user_id": reaction["user_id"], "post_id": post, "emoji_name": reaction["emoji_name"]})})

    thread.join()
    ws.join()

if __name__ == "__main__":
    main()
