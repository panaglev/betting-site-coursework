import sqlite3

create_users = '''CREATE TABLE "users" (
				"user_id"	INTEGER NOT NULL UNIQUE, 
				"login"	TEXT NOT NULL UNIQUE, 
				"pass_hash"	TEXT NOT NULL, 
				"balance"	REAL, 
				PRIMARY KEY("user_id" AUTOINCREMENT)
				);'''

create_sports = '''CREATE TABLE "sports" (
				"sport_id"	INTEGER NOT NULL UNIQUE,
				"sport_type"	TEXT NOT NULL UNIQUE,
				PRIMARY KEY("sport_id" AUTOINCREMENT)
				);'''

create_teams = '''CREATE TABLE "teams" (
				"team_id"	INTEGER NOT NULL UNIQUE,
				"sport_id"	INTEGER NOT NULL,
				"team_name"	TEXT NOT NULL,
				FOREIGN KEY("sport_id") REFERENCES "sports"("sport_id"),
				PRIMARY KEY("team_id" AUTOINCREMENT)
				);''' 

create_events = '''CREATE TABLE "events" (
				"event_id"	INTEGER NOT NULL UNIQUE,
				"team1_id"	INTEGER NOT NULL,
				"team2_id"	INTEGER NOT NULL,
				"event_status"	INTEGER NOT NULL,
				"winner"	INTEGER,
				PRIMARY KEY("event_id" AUTOINCREMENT),
				FOREIGN KEY("team2_id") REFERENCES "teams"("team_id"),
				FOREIGN KEY("team1_id") REFERENCES "teams"("team_id")
				);'''

create_bets = '''CREATE TABLE "bets" (
				"bet_id"	INTEGER NOT NULL UNIQUE,
				"user_id"	INTEGER NOT NULL,
				"bet_amount"	INTEGER,
				PRIMARY KEY("bet_id" AUTOINCREMENT),
				FOREIGN KEY("user_id") REFERENCES "users"("user_id")
				);'''

create_betsevents = '''CREATE TABLE "betsevents" (
					"betsevents_id"	INTEGER NOT NULL UNIQUE,
					"bets_id"	INTEGER NOT NULL,
					"event_id"	INTEGER NOT NULL,
					PRIMARY KEY("betsevents_id" AUTOINCREMENT),
					FOREIGN KEY("event_id") REFERENCES "events"("event_id"),
					FOREIGN KEY("bets_id") REFERENCES "bets"("bet_id")
					);'''
	
with sqlite3.connect("coursework.db") as connection:
	cursor = connection.cursor()
	cursor.execute(create_users)
	cursor.execute(create_sports)
	cursor.execute(create_teams)
	cursor.execute(create_events)
	cursor.execute(create_bets)
	cursor.execute(create_betsevents)
	connection.commit()
print("Done!")