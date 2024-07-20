import sqlite3

# to create a database
with sqlite3.connect("insurance.db") as connection:
    # varchar(10)
    query = """CREATE TABLE IF NOT EXISTS project (name TEXT, Email TEXT, age TEXT,bmi TEXT,chl TEXT,rgn TEXT,smk TEXT,gen TEXT,hlt TEXT, predict TEXT)"""
    cur = connection.cursor()
    cur.execute(query)

print("table created")
fetch_data_query = "SELECT * FROM project"
with sqlite3.connect("insurance.db") as connection:
    cur = connection.cursor()
    cur.execute(fetch_data_query)
    rows = cur.fetchall()

# Print all fetched data
for row in rows:
    print(row)
# print(rows[-1])