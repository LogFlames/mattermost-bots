# Undelete message

Use `python3 scripts/fohsar_messages_to_detele_and_undelete.py`. Keep the post lists
in that script's `blacklisted_messages_*` dictionaries.

- **D** deletes the listed posts through Mattermost and saves a timestamped `.log`
  under `scripts/deleted_messages/`, regardless of the current directory. It requires
  `scripts/secret.py` with a `TOKEN` belonging to a system administrator, including
  permission to read deleted posts to confirm each deletion.
- **U** takes a filename from that directory and prints a PostgreSQL transaction.
  It does not connect to Mattermost or execute SQL, and needs no token.
- **q** quits.

New logs contain JSON lines: a flushed, fsynced snapshot before each deletion and
a confirmation with the server's deletion timestamp afterward. They record active
post IDs, root IDs, active attachment IDs, the original `deleteBy` property, and the
deleting user. They contain no message bodies or attachment contents. Deleting a
reply logs only that reply; deleting a root logs its active thread. Already-deleted
replies and attachments are not restoration targets. Roots are processed before
listed replies, and temporarily unarchived channels are rearchived in a `finally`
block. Log files are created with owner-only permissions; keep a backup.

The generated transaction restores only still-deleted posts whose deletion timestamp,
update timestamp, root and deleting user match the new log. It restores recorded
attachments, restores the original `deleteBy` property without replacing unrelated
properties, advances `updateat` for client synchronization, clears restored roots'
thread-deletion flags, and recalculates affected thread counts, latest-reply times
and participants from active replies. Unlisted deleted replies remain deleted.
Already-visible posts are left alone. This is not a byte-for-byte database backup:
old timestamps overwritten by a root's deletion cascade cannot be recovered.

If deletion or confirmation fails, the log retains the prepared operation. **U
refuses incomplete logs.** Inspect the affected posts and channel state before
reconciling that log; do not drop an unconfirmed record and assume deletion failed.

Old one-ID-per-line logs, including `M26_cleanup_20260824.log`, are still accepted
and deduplicated. They have no deletion timestamps or attachment snapshots, so the
SQL includes a warning: inspect the current deletion state before executing it.
Legacy restoration undeletes all attachments linked to the selected deleted posts;
it cannot distinguish attachments deleted before the cleanup or later post deletions.

**Review and approve the generated SQL before running it against production.** Back
up the affected database state, then connect using `ssh fmm` and run the reviewed
SQL with `sudo -u postgres psql -X -v ON_ERROR_STOP=1 -d mattermost`. The output is
a psql script; copy only the generated SQL, not the interactive prompts. Errors
abort the transaction; do not manually commit a failed or partially executed script.

SQL restoration does not publish websocket events, clear server caches, or rebuild
external search indexes. Handle cache invalidation and any reindexing separately;
clients need to refetch the affected channels/threads. Archived channels stay archived.

Run the tests with `python3 -m unittest discover -s scripts -p 'test_fohsar_messages.py'`.
For SQL integration tests, set `RECEPTION_TEST_DSN` to a **disposable local PostgreSQL
database** with permission to create schemas. These tests create and drop isolated
schemas. Never point it at production.

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
