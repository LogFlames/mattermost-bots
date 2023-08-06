from eliasmamo import *
from ws import WebSocket
from secret import TOKEN

user_id = "xzt5e9rmtb8b5c78auq3h7bffr"
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

enable_all_notifications(driver, user_id)
