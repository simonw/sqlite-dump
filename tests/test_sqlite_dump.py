from sqlite_dump import iterdump
import sqlite3
import sqlite_utils
import pytest


@pytest.fixture()
def db_path(tmpdir):
    path = str(tmpdir / "test.db")
    db = sqlite_utils.Database(path)
    db["dogs"].insert_all(
        [{"id": 1, "name": "Cleo", "age": 5}, {"id": 2, "name": "Pancakes", "age": 4}],
        pk="id",
    )
    return path


def test_example_function(db_path):
    conn = sqlite3.connect(db_path)
    lines = list(iterdump(conn))
    assert lines == [
        "BEGIN TRANSACTION;",
        "CREATE TABLE [dogs] (\n   [id] INTEGER PRIMARY KEY,\n   [name] TEXT,\n   [age] INTEGER\n);",
        "INSERT INTO \"dogs\" VALUES(1,'Cleo',5);",
        "INSERT INTO \"dogs\" VALUES(2,'Pancakes',4);",
        "COMMIT;",
    ]
