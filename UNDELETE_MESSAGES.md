# Undelete message

SSH to [mattermost.fysiksektionen.se](mattermost.fysiksektionen.se) as root

Connect to database
```
su - postgres
psql
\c mattermost
```

Then normal SQL querys, strings must be in `'`.

Undelete one message:
```
UPDATE posts SET deleteat = 0 WHERE id='chowcd1f7bni9xs6mnc1ttwgny'
```

Undelete multiple messages:
```
UPDATE posts SET deleteat = 0
WHERE id IN ('chowcd1f7bni9xs6mnc1ttwgny',...);
```

## Be Careful! This writes directly to PROD!!! Do not undelete every message on the server for example :)

### Some postgres help

```
\l - lists databases
\c [database] - connects to database
\dt - lists tables
\d+ [table] - shows more information on specific table
```

[Here](https://www.postgresqltutorial.com/postgresql-cheat-sheet/) is a postgres sheet-cheat if needed.

# Transfer message ownership

Update user ids in [transfer_userid_ownership.py](scripts/transfer_userid_ownership.py). Run script. Copy the 3 SQL-queries directly to psql.

If you wish to record the post-ids for safety when restoring these can be accessed using:
```
\pset pager 0
select id from posts where userid='fake_account_id';
```

## Be Careful! This writes directly to PROD!!! Do not undelete every message on the server for example :)