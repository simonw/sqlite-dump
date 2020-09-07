# Adapted from code written by Paul Kippes and released as
# part of the Python standard library, see
# https://github.com/python/cpython/blob/v3.8.5/Lib/sqlite3/dump.py


def iterdump(connection):
    cu = connection.cursor()
    yield "BEGIN TRANSACTION;"

    writable_schema = False

    q = """
    SELECT "name", "type", "sql"
    FROM "sqlite_master"
        WHERE "sql" NOT NULL AND
        "type" == 'table'
        ORDER BY "name"
    """
    schema_res = cu.execute(q)
    for table_name, type, sql in schema_res.fetchall():
        if table_name == "sqlite_sequence":
            yield ('DELETE FROM "sqlite_sequence";')
        elif table_name == "sqlite_stat1":
            yield ('ANALYZE "sqlite_master";')
        elif table_name.startswith("sqlite_"):
            continue
        elif sql.startswith("CREATE VIRTUAL TABLE"):
            if not writable_schema:
                yield "PRAGMA writable_schema=ON;"
                writable_schema = True
            qtable = table_name.replace("'", "''")
            yield (
                "INSERT INTO sqlite_master(type,name,tbl_name,rootpage,sql) "
                "VALUES('table','{0}','{0}',0,'{1}');"
            ).format(qtable, sql)
            # Skip the bit that writes the INSERTs for this table
            continue
        else:
            yield "{0};".format(sql)

        # Build the insert statement for each row of the current table
        table_name_ident = table_name.replace('"', '""')
        res = cu.execute('PRAGMA table_info("{0}")'.format(table_name_ident))
        column_names = [str(table_info[1]) for table_info in res.fetchall()]
        q = """SELECT 'INSERT INTO "{0}" VALUES({1})' FROM "{0}";""".format(
            table_name_ident,
            ",".join(
                """'||quote("{0}")||'""".format(col.replace('"', '""'))
                for col in column_names
            ),
        )
        query_res = cu.execute(q)
        for row in query_res:
            yield "{0};".format(row[0])

    # Now when the type is 'index', 'trigger', or 'view'
    q = """
    SELECT "name", "type", "sql"
    FROM "sqlite_master"
        WHERE "sql" NOT NULL AND
        "type" IN ('index', 'trigger', 'view')
    """
    schema_res = cu.execute(q)
    for name, type, sql in schema_res.fetchall():
        yield "{0};".format(sql)

    if writable_schema:
        yield "PRAGMA writable_schema=OFF;"

    yield "COMMIT;"
