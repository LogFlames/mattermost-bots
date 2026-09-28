from eliasmamo_import import *
import logging
from secret import TOKEN
from configuration import CHANNEL_ID, HISTORY_MESSAGE_ID, SPREADSHEET_ID
import time

import os.path

logger = logging.getLogger(__name__)

from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
RANGE_NAME = 'B2:D'

def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.join(os.path.dirname(__file__), 'token.json')):
        creds = Credentials.from_authorized_user_file(os.path.join(os.path.dirname(__file__), 'token.json'), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(os.path.join(os.path.dirname(__file__), 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(os.path.join(os.path.dirname(__file__), 'token.json'), 'w') as token:
            token.write(creds.to_json())

    return creds

def create_service():
    return build('sheets', 'v4', credentials=get_credentials(), cache_discovery=False) # oauthclient2 might not support cache_discovery

def read_sheet(service):

    try:
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            logger.info('No data found.')
            return []

        return [f"@channel {row[0]} {row[1]} har sökt {row[2]}" for row in values]
    except RefreshError:
        logger.exception('Google credentials have expired or been revoked.')
        return None
    except HttpError as err:
        logger.exception(err)

def read_history(driver):
    message = driver.posts.get_post(HISTORY_MESSAGE_ID)["message"]
    if len(message) < 6: # assume empty / uninitialized
        write_history(driver, [])
        logger.info(f"Corrected history, assumed empty.")
        return []
    if message.startswith("```") and message.endswith("```"):
        message = message[3:-3].strip()
    if message == "History is empty.":
        logger.info(f"History read and is empty.")
        return []
    logger.info(f"Non-empty history read.")
    return message.splitlines() if message else []

def write_history(driver, values):
    message = "\n".join(values) if values else "History is empty."
    message = f"```\n{message}\n```"
    driver.posts.update_post(
        HISTORY_MESSAGE_ID,
        {"id": HISTORY_MESSAGE_ID, "message": message},
    )

def main():
    logging.basicConfig(level=logging.INFO)
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

    service = create_service()
    history = read_history(driver)
    values = read_sheet(service)
    if values is not None:
        logger.info(f"Can read sheet values.")

    while True:
        time.sleep(20)
        values = read_sheet(service)

        if values is None:
            logger.error(f"Failed to read sheet values")
            continue

        history_updated = False
        for row in values:
            if row not in history:
                driver.posts.create_post({"channel_id": CHANNEL_ID, "message": row})
                history_updated = True
                logger.info(f"Sent message: \"{row}\"")

        if history_updated:
            write_history(driver, values)
            history = read_history(driver)

if __name__ == "__main__":
    main()
