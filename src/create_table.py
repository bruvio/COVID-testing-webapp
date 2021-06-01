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

create_table = "CREATE TABLE IF NOT EXISTS cartridges ( cartridgeId text PRIMARY KEY, testStatus text, departmentName text, boxName text, pattern text, hospitalName text, operatorName text,    organisationId text,   participantId text, trustName text,    submissionDateTime datetime,    testStartDateTime datetime,    lastUpdatedDateTime datetime)"
cursor.execute(create_table)


sqlite_insert_query = """INSERT INTO cartridges
                          (cartridgeId, testStatus,departmentName, boxName, pattern, hospitalName,
                           operatorName,organisationId,participantId,trustName,submissionDateTime,testStartDateTime,lastUpdatedDateTime)
                           VALUES
                          ('DN41100041459077',
	 'Complete',
	 'DPT001',
	'nudge_2294DC',
	 'CVD540',
	 'HSP001',
	 'opt1',
	 'ORG1',
	 'V8Z85',
	 'TRUST1',
	 '2021-03-04 10:59:40.000 UTC',
	 '2021-03-04 11:01:55.000 UTC',
	 '2021-03-04 12:45:58.192 UTC')"""


cursor.execute(sqlite_insert_query)


connection.commit()

connection.close()
print("DONE")
