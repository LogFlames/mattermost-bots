from eliasmamo_import import *
from secret import TOKEN
from configuration import *
import os
import datetime
from mattermostdriver.exceptions import ResourceNotFound

messages_from_matwan = ('i3mimqq3djd4iy95o77wbdcd8a', 'mbd43kbx4pfmzc1w3w1p36yaye', 'ezmpb5jdw78ax8cdjxyoii5nuo')
messages_from_sael = ('xj3hucrrdtb87e3jdbjx74ndha', '4j8fkgg6ff8ujmk1qjcscn8q7h', 'zhcxtbu44f8sbnz8wpzt1u9uta', '58s7xrcgp3gnin75aor6gf98po', 'da99n6pgdfypmd7eypdqk7j1sa')
messages_from_emmakt = ()
messages_from_lagehl = ('mrne9w9ur7fqjbiqyfjkn7nh9o', )
messages_from_fiek = ('gdjwfnhjjfn7fpz9x13z68xd4w', )
messages_from_kajsaeng = ('t8zgua7g33gjmy7jpniwhby35e', )
messages_from_lijanes = ('jmigo3ngi3rdmpbzjb9higydkw', )

messages_to_delete = (*messages_from_matwan,
                      *messages_from_sael,
                      *messages_from_emmakt,
                      *messages_from_lagehl,
                      *messages_from_fiek,
                      *messages_from_kajsaeng,
                      *messages_from_lijanes)

def main():
    while (ans := input("(D). Delete messages\n(U). Generate Update Query \n(q). Quit\nWhat do you want to do?: ")) not in ("D", "U", "q"): pass
    if ans == "D":
        deleted_messages = set()
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
            try:
                driver.posts.get_post(message)
            except ResourceNotFound:
                print(f"Could not find message: {message}")
                continue
            for post in driver.posts.get_thread(message)['posts'].keys():
                deleted_messages.add(post)
            print(f"Deleting message: {message}")
            driver.posts.delete_post(message)

        if len(deleted_messages) == 0:
            print("Did not delete any messages")
            exit(1)

        if not os.path.exists("deleted_messages/"):
            os.mkdir("deleted_messages/")

        name = f"deleted_messages/deleted_messages_at-{datetime.datetime.now()}.log"
        with open(name, "w+") as log:
            posts = "\n".join(deleted_messages)
            log.write(f"{posts}\n")

        print(f"Deleted messages written to file: {name}")

    elif ans == "U":
        p = input("Path to file with messages (excluding 'deleted_messages/'): ")
        pp = os.path.join(os.path.dirname(__file__), "deleted_messages/", p)
        if not os.path.exists(pp):
            print(f"Could not find file: {pp}")
            exit(1)

        with open(pp, "r") as f:
            messages = f.read().split()
        posts = "', '".join(messages)
        print(f"UPDATE posts SET deleteat = 0 WHERE id IN ('{posts}');")

if __name__ == "__main__":
    main()

