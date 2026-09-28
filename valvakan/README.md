# Valvakan bot

Posts a Mattermost @channel message whenever a new person appears in the election application spreadsheet.

The bot:
- reads the configured Google Sheet,
- checks for new rows,
- posts only new entries to the target channel,
- stores a history message to avoid reposting duplicates.

It polls the sheet every 20 seconds and sends messages in the format:

@channel <first name> <last name> har sökt <value>

Setup:
1. Copy `example_secret.py` to `secret.py` and add the Mattermost token.
2. Update `configuration.py` with the target channel, spreadsheet ID, and history message ID.
3. Run the bot once to complete the Google OAuth flow and generate `token.json`.
