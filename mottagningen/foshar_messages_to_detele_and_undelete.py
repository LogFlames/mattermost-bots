from eliasmamo_import import *
from secret import TOKEN
from configuration import *

messages_to_delete = ()

def main():
    while (ans := input("(D). Delete messages\n(U). Generate Update Query \n(q). Quit\nWhat do you want to do?: ")) not in ("D", "U", "q"): pass
    if ans == "D":
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

        for message in messages_to_delete:
            driver.posts.delete_post(message)
    elif ans == "U":
        posts = "', '".join(messages_to_delete)
        print(f"UPDATE posts SET deleteat = 0 WHERE id IN ('{posts}')")

if __name__ == "__main__":
    main()

