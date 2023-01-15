import sqlite3

with sqlite3.connect("coursework.db") as connection:
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE "users" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"login"	TEXT NOT NULL UNIQUE,
	"pass_hash"	TEXT NOT NULL,
	"balance"	REAL,
	PRIMARY KEY("user_id" AUTOINCREMENT)
);''')
    connection.commit()

print("Done!")