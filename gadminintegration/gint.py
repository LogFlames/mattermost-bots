import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/admin.directory.group"]

def get_group_members(group, recursive = False, include_subgroups = False):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(os.path.join(os.path.dirname(__file__), "token.json")):
        creds = Credentials.from_authorized_user_file(os.path.join(os.path.dirname(__file__), "token.json"), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(os.path.dirname(__file__), "credentials.json"), SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(os.path.join(os.path.dirname(__file__), "token.json"), "w") as token:
            token.write(creds.to_json())

    try:
        service = build("admin", "directory_v1", credentials = creds)
        members = []

        res = service.members().list(groupKey = group, includeDerivedMembership = recursive, maxResults = 200).execute()
        members.extend(res["members"])

        while "nextPageToken" in res:
            res = service.members().list(groupKey = group, includeDerivedMembership = recursive, maxResults = 200, pageToken = res["nextPageToken"]).execute()

            if "members" in res:
                members.extend(res["members"])
        if not include_subgroups:
            members = list(filter(lambda x: x["type"] != "GROUP", members))

        members = set(map(lambda x: x["email"], members))

        return members
    except HttpError as err:
        print(err)
        return set()
