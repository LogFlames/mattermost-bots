from threading import Thread
import unicodedata
import openpyxl
import os
import re

from eliasmamo_import import *
from secret import TOKEN
from configuration import TEAM_ID

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

    dataframe = openpyxl.load_workbook(os.path.join(os.path.dirname(__file__), "kursutdrag", "VT24_p3.xlsx"), read_only = True)

    #### Config
    sheet_name = "Sheet1"
    program_column = 1
    kth_id_column = 2
    course_code_column = 6
    course_name_column = 7

    if sheet_name not in dataframe.sheetnames:
        print(f"Could not find '{sheet_name}' among the sheets, available sheets are: {dataframe.sheetnames}.")
        return

    sheet = dataframe[sheet_name]

    print(f"Using columns with headers: ")
    print(f"    Program: {sheet.cell(row = 1, column = program_column).value}")
    print(f"    KTH id: {sheet.cell(row = 1, column = kth_id_column).value}")
    print(f"    Course code: {sheet.cell(row = 1, column = course_code_column).value}")
    print(f"    Course name: {sheet.cell(row = 1, column = course_name_column).value}")
    confirmation = input("Please confirm this looks right? (y/N): ")
    if confirmation not in ["y", "Y", "yes", "Yes"]:
        return

    users = {}
    for user in get_all_users(driver):
        users[user["username"]] = user["id"]

    channels = {}
    for channel in get_all_public_channels(driver, TEAM_ID):
        channels[channel["name"]] = channel["id"]
        print(channel["name"])

    skipped_kth_ids = set()

    for row in sheet.iter_rows(2):
        kth_mail = str(row[kth_id_column - 1].value)
        kth_id = kth_mail.replace("@kth.se", "")

        if kth_id in skipped_kth_ids:
            continue

        if kth_id not in users:
            print(f"{kth_id} does not have a mattermost account. Skipping...")
            skipped_kth_ids.add(kth_id)
            continue

        course_code = str(row[course_code_column - 1].value)
        course_name = str(row[course_name_column - 1].value)

        if "null" in course_code or "null" in course_name:
            print(f"{kth_id}: Either course_code or course_name equals 'null', skipping...")
            continue

        channel_name = f"{course_code.lower()}-{course_name.lower().replace(' ', '-')}"
        channel_name = unicodedata.normalize("NFKD", channel_name).encode("ascii", errors = "ignore").decode("ascii")

        channel_name = re.sub(r"[^a-z0-9-]", "", channel_name)

        channel_name = channel_name[:64] # Mattermost has a limit of 64 characters in the channel url

        if channel_name == "dd1331-grundlaggande-programmering":
            channel_name += "-" + str(row[program_column - 1].value).lower()

        if channel_name not in channels:
            ans = input(f"Missing channel f{channel_name}, create a new channel? (y/N): ")
            if ans not in ["y", "Y", "yes", "Yes"]:
                print(f"Not creating a new channel. Skipping course for user...")
                continue
            print(f"Creating new channel {channel_name}")
            new_channel = driver.channels.create_channel({"team_id": TEAM_ID, "name": channel_name, "display_name": f"{course_code} {course_name}", "type": "O"})
            channels[channel_name] = new_channel["id"]

        if channel_name not in channels:
            continue
        
        print(f"Adding user {kth_id} to channel {channel_name}...")
        driver.channels.add_user(channels[channel_name]["id"], {"user_id": users[kth_id]})

if __name__ == "__main__":
    main()
