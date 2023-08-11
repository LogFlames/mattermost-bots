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
