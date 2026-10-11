import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
import uuid


spec = importlib.util.spec_from_file_location(
    "cleanup", Path(__file__).with_name("fohsar_messages_to_detele_and_undelete.py")
)
cleanup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleanup)
ROOT, REPLY, OLD, OTHER, FILE, OLD_FILE, ACTOR, AUTHOR = [letter * 26 for letter in "abcdefgh"]


class FakeMattermost:
    def __init__(self, fail=False):
        self.data = {
            ROOT: {"id": ROOT, "root_id": "", "delete_at": 0, "props": {}, "file_ids": [FILE, OLD_FILE]},
            REPLY: {"id": REPLY, "root_id": ROOT, "delete_at": 0, "props": {"deleteBy": "old'actor"}},
            OLD: {"id": OLD, "root_id": ROOT, "delete_at": 40, "props": {}},
        }
        for post in self.data.values():
            post["channel_id"] = OTHER
        self.archived = True
        self.fail = fail
        self.client = SimpleNamespace(get=self.get, userid=ACTOR)
        self.posts = SimpleNamespace(get_thread=self.get_thread, delete_post=self.delete)
        self.files = SimpleNamespace(get_file_metadata=lambda fid: {
            "id": fid, "post_id": ROOT, "delete_at": 40 if fid == OLD_FILE else 0,
        })
        self.channels = SimpleNamespace(
            get_channel=lambda _: {"id": OTHER, "delete_at": 99 if self.archived else 0},
            restore_channel=lambda _: setattr(self, "archived", False),
            delete_channel=lambda _: setattr(self, "archived", True),
        )

    def get(self, endpoint, params):
        return copy.deepcopy(self.data[endpoint.split("/")[-1]])

    def get_thread(self, post_id):
        return {"posts": copy.deepcopy({key: post for key, post in self.data.items() if post["delete_at"] == 0})}

    def delete(self, post_id):
        if self.fail:
            raise RuntimeError("Deletion failed")
        for post in self.data.values():
            if post["id"] == post_id or post["root_id"] == post_id:
                post["delete_at"] = 100
                post["props"]["deleteBy"] = ACTOR


def deletion_log(ids=(REPLY, ROOT), fail=False):
    driver = FakeMattermost(fail)
    with tempfile.TemporaryFile(mode="w+") as log:
        with patch.object(cleanup.time, "sleep"), contextlib.redirect_stdout(io.StringIO()):
            try:
                cleanup.delete_messages(driver, ids, log)
            except RuntimeError:
                if not fail:
                    raise
        log.seek(0)
        return driver, log.read()


class JournalTests(unittest.TestCase):
    def test_root_cascade_records_only_active_posts_and_attachments(self):
        driver, text = deletion_log()
        prepared, deleted = map(json.loads, text.splitlines())
        self.assertEqual({post["id"] for post in prepared["posts"]}, {ROOT, REPLY})
        self.assertEqual(prepared["files"], [FILE])
        self.assertEqual(deleted["deleteat"], 100)
        self.assertTrue(driver.archived)
        cleanup.generate_restore_sql(text)

    def test_reply_only_does_not_log_siblings_or_root(self):
        _, text = deletion_log((REPLY,))
        record = json.loads(text.splitlines()[0])
        self.assertEqual([post["id"] for post in record["posts"]], [REPLY])

    def test_failure_preserves_intent_rearchives_and_refuses_restore(self):
        driver, text = deletion_log(fail=True)
        self.assertEqual(json.loads(text)["event"], "prepared")
        self.assertTrue(driver.archived)
        with self.assertRaisesRegex(ValueError, "Incomplete"):
            cleanup.generate_restore_sql(text)

    def test_legacy_and_invalid_logs(self):
        for path in Path(__file__).with_name("deleted_messages").glob("*.log"):
            cleanup.generate_restore_sql(path.read_text())
        for invalid in ["", "not-a-post-id", ROOT + "'; DELETE FROM posts;--"]:
            with self.assertRaises(ValueError):
                cleanup.generate_restore_sql(invalid)


@unittest.skipUnless(os.environ.get("RECEPTION_TEST_DSN"), "Set RECEPTION_TEST_DSN to a disposable PostgreSQL database")
class RestoreSQLTests(unittest.TestCase):
    def sql(self, sql, check=True):
        return subprocess.run(
            ["psql", "-X", "-qAt", "-v", "ON_ERROR_STOP=1", os.environ["RECEPTION_TEST_DSN"]],
            input=f"SET search_path TO {self.schema};\n" + sql,
            text=True, capture_output=True, check=check,
        )

    def setUp(self):
        self.schema = "restore_test_" + uuid.uuid4().hex
        self.sql(f"CREATE SCHEMA {self.schema};")
        self.addCleanup(lambda: self.sql(f"DROP SCHEMA {self.schema} CASCADE;"))
        self.sql(f"""
            CREATE TABLE posts (id text PRIMARY KEY, rootid text, userid text,
                createat bigint, updateat bigint, deleteat bigint, props jsonb);
            CREATE TABLE fileinfo (id text PRIMARY KEY, postid text, deleteat bigint);
            CREATE TABLE threads (postid text PRIMARY KEY, replycount bigint,
                lastreplyat bigint, participants jsonb, threaddeleteat bigint);
            INSERT INTO posts VALUES
                ('{ROOT}', '', '{ACTOR}', 1, 100, 100, '{{"deleteBy":"{ACTOR}","other":true}}'),
                ('{REPLY}', '{ROOT}', '{AUTHOR}', 20, 100, 100, '{{"deleteBy":"{ACTOR}"}}'),
                ('{OLD}', '{ROOT}', '{ACTOR}', 30, 100, 100, '{{"deleteBy":"{ACTOR}"}}'),
                ('{OTHER}', '', '{AUTHOR}', 40, 50, 50, '{{}}');
            INSERT INTO fileinfo VALUES ('{FILE}','{ROOT}',101), ('{OLD_FILE}','{ROOT}',100);
            INSERT INTO threads VALUES ('{ROOT}',0,0,'[]',100);
        """)

    def test_roundtrip_restores_only_snapshot_and_is_idempotent(self):
        _, text = deletion_log()
        sql = cleanup.generate_restore_sql(text)
        self.sql(sql)
        result = json.loads(self.sql(f"""SELECT json_build_object(
            'live', (SELECT json_agg(id ORDER BY id) FROM posts WHERE deleteat=0),
            'files', (SELECT json_agg(id) FROM fileinfo WHERE deleteat=0),
            'root_props', (SELECT props FROM posts WHERE id='{ROOT}'),
            'reply_props', (SELECT props FROM posts WHERE id='{REPLY}'),
            'count', (SELECT replycount FROM threads),
            'last', (SELECT lastreplyat FROM threads),
            'participants', (SELECT participants FROM threads),
            'hidden', (SELECT threaddeleteat FROM threads),
            'new_version', (SELECT bool_and(updateat>100) FROM posts WHERE deleteat=0)
        );""").stdout)
        self.assertEqual(result, {
            "live": [ROOT, REPLY], "files": [FILE], "root_props": {"other": True},
            "reply_props": {"deleteBy": "old'actor"}, "count": 1, "last": 20,
            "participants": [AUTHOR], "hidden": 0, "new_version": True,
        })
        before = self.sql("SELECT json_agg(p ORDER BY id) FROM posts p;").stdout
        self.sql(sql)
        self.assertEqual(self.sql("SELECT json_agg(p ORDER BY id) FROM posts p;").stdout, before)

    def test_reply_restore_keeps_visible_root_and_newer_replies(self):
        _, text = deletion_log((REPLY,))
        sibling = "i" * 26
        self.sql(f"""
            UPDATE posts SET deleteat=0,updateat=50,props='{{"other":true}}' WHERE id='{ROOT}';
            INSERT INTO posts VALUES ('{sibling}','{ROOT}','{ACTOR}',60,60,0,'{{}}');
            UPDATE threads SET replycount=1,lastreplyat=60,participants='["{ACTOR}"]',threaddeleteat=0;
        """)
        self.sql(cleanup.generate_restore_sql(text))
        result = json.loads(self.sql(f"""SELECT json_build_object(
            'root_version', (SELECT updateat FROM posts WHERE id='{ROOT}'),
            'count', (SELECT replycount FROM threads),
            'last', (SELECT lastreplyat FROM threads),
            'participants', (SELECT participants FROM threads),
            'restored_files', (SELECT count(*) FROM fileinfo WHERE deleteat=0)
        );""").stdout)
        self.assertEqual(result, {"root_version": 50, "count": 2, "last": 60,
                                  "participants": [AUTHOR, ACTOR], "restored_files": 0})

    def test_later_deletion_rolls_back_whole_restore(self):
        _, text = deletion_log()
        self.sql(f"UPDATE posts SET deleteat=200,updateat=200 WHERE id='{REPLY}';")
        result = self.sql(cleanup.generate_restore_sql(text), check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Post state differs", result.stderr)
        self.assertEqual(self.sql("SELECT count(*) FROM posts WHERE deleteat=0;").stdout.strip(), "0")

    def test_legacy_deduplicates_ids_without_restoring_unlisted_posts(self):
        self.sql(cleanup.generate_restore_sql(f"{ROOT}\n{REPLY}\n{ROOT}\n"))
        self.assertEqual(self.sql("SELECT count(*) FROM posts WHERE deleteat=0;").stdout.strip(), "2")
        self.assertEqual(self.sql(f"SELECT deleteat FROM posts WHERE id='{OLD}';").stdout.strip(), "100")


if __name__ == "__main__":
    unittest.main()
