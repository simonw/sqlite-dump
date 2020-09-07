from sqlite_dump import iterdump
import sqlite3
import sqlite_utils
import pytest


@pytest.fixture()
def db_and_path(tmpdir):
    path = str(tmpdir / "test.db")
    db = sqlite_utils.Database(path)
    db["dogs"].insert_all(
        [{"id": 1, "name": "Cleo", "age": 5}, {"id": 2, "name": "Pancakes", "age": 4}],
        pk="id",
    )
    return db, path


def test_basic(db_and_path):
    db, path = db_and_path
    conn = sqlite3.connect(path)
    lines = list(iterdump(conn))
    assert lines == [
        "BEGIN TRANSACTION;",
        "CREATE TABLE IF NOT EXISTS [dogs] (\n   [id] INTEGER PRIMARY KEY,\n   [name] TEXT,\n   [age] INTEGER\n);",
        "INSERT INTO \"dogs\" VALUES(1,'Cleo',5);",
        "INSERT INTO \"dogs\" VALUES(2,'Pancakes',4);",
        "COMMIT;",
    ]


@pytest.mark.parametrize("fts_version", ["FTS4", "FTS5"])
def test_fts(db_and_path, tmpdir, fts_version):
    db, path = db_and_path
    db["dogs"].enable_fts(["name"], fts_version=fts_version)
    conn = sqlite3.connect(path)
    lines = list(iterdump(conn))
    db2_path = str(tmpdir / "restored.db")
    conn2 = sqlite3.connect(db2_path)
    conn2.executescript("\n".join(lines))
    db2 = sqlite_utils.Database(conn2)
    assert list(db2["dogs"].rows) == [
        {"id": 1, "name": "Cleo", "age": 5},
        {"id": 2, "name": "Pancakes", "age": 4},
    ]
    assert db2["dogs"].detect_fts() == "dogs_fts"
    assert db2["dogs_fts"].schema == (
        "CREATE VIRTUAL TABLE [dogs_fts] USING {} (\n".format(fts_version)
        + "                [name],\n"
        + "                content=[dogs]\n"
        + "            )"
    )
