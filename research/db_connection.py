import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
try:
    testing_table = c.execute("PRAGMA table_info(test_connection)")
    print(testing_table.fetchall())
    c.execute("DROP TABLE test_connection")
    # c.execute("ALTER TABLE test_connection DROP COLUMN name")
    # c.execute("ALTER TABLE test_connection DROP COLUMN date")
    testing_table2 = c.execute("PRAGMA table_info(test_connection)")
    print(testing_table2.fetchall())
    conn.close()
except:
    c.execute("CREATE TABLE test_connection IF NOT EXISTS (products VARCHAR(100), complaints VARCHAR(5000))")
    conn.close()