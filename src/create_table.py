import os
import sqlite3

try:
    os.remove("data.db")
except:
    pass
connection = sqlite3.connect("data.db")

cursor = connection.cursor()

# id INTEGER PRIMARY KEY CREATES AUTO incrementing column id
# so we will only have to specify username and password when creating an user
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)
cursor.execute("INSERT INTO users VALUES (1,'bruno', 'asdf')")

create_table = (
    "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)"
)
cursor.execute(create_table)
cursor.execute("INSERT INTO items VALUES (1, 'test', 10.99)")


connection.commit()

connection.close()
print("DONE")
