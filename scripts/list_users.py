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

    users = get_all_users(driver)

    for user in users:
        # print(f"{user['id']: <16} {user['username']: <20} {user['first_name']} {user['last_name']}")
        print(f"{user['id']: <16} {user['first_name']} {user['last_name']}")

if __name__ == "__main__":
    main()
