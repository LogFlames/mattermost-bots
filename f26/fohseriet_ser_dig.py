from eliasmamo_import import *
from secret import TOKEN
import time
from threading import Thread

FOHSARE = ("1a7a3s9um78p98zsz1k35a5k8r", "5d85r8gsn7dcjyeo48o4j41cjo", "76n3u5yp9tb53mnsjcky7rs9ih")

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
