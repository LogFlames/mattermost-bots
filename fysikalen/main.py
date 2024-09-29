from eliasmamo_import import *
from secret import TOKEN
from datetime import datetime

COUNTDOWN_CHANNEL = "5iqn98qidtfe8k9cmxfp5zs1wh"

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

    diff = (datetime.fromisoformat("2025-04-13T00:00:00.000000") - datetime.today())
    dagar = diff.days + 1

    message = f"{dagar} dag{'ar' if dagar != 1 else ''} kvar till premiären!"
    print(message)

if __name__ == "__main__":
    main()
