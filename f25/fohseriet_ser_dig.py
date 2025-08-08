from eliasmamo_import import *
from secret import TOKEN
import time
from threading import Thread

FOHSARE = ("adt5q1g55i8dbnorfmdmp367dy", "fixxox8xyjb9dm8cffikeitgew", "cwewz5kw1jdkzxi7z1cqfhof5e")

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

    always_online_thread = Thread(target = lambda: update_user_status(driver))
    always_online_thread.start()

    always_online_thread.join()

if __name__ == "__main__":
    main()
