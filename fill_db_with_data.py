import sqlite3
#cursor.execute("INSERT INTO users (login, pass_hash, balance) VALUES ('%s', '%s', 0);"%(login, password,))

fill_sports = '''INSERT INTO sports (sport_type) VALUES ("Box"), ("Drift"), ("Dota 2"), ("CS:GO"), ("F1");'''

fill_teams = '''INSERT INTO teams (sport_id, team_name) VALUES 
                (1, "Oleksandr Usyk"),
                (2, "Arkadiy Tsaregradsev"),
                (3, "Tundra"),
                (4, "G2 Esports"),
                (5, "Max Verstappen"),
                (1, "Tyson Fury"),
                (2, "Georgiy Chivchyan"),
                (3, "Darkside"),
                (4, "Navi"),
                (5, "Lewis Hamilton");'''

fill_events = '''INSERT INTO events (team1_id, team2_id, event_status) VALUES 
                (1, 6, 0),
                (2, 7, 0),
                (3, 8, 0),
                (4, 9, 0),
                (5, 10, 0);'''

fill_users = '''INSERT INTO users (login, pass_hash, balance) VALUES 
                ("Admin", "713bfda78870bf9d1b261f565286f85e97ee614efe5f0faf7c34e7ca4f65baca", 1000), 
                ("Kolya_Tri_Uha", "05d49692b755f99c4504b510418efeeeebfd466892540f27acf9a31a326d6504", 1000),
                ("Vasya_Mask_of_Madness", "c745dda06acd95763dd9604e15acebd0ca48a276f95d68c00233eb1acf37ed73", 1000),
                ("Stalker_1337", "9bd384c77ed0641dd62109eff7ae2be206d02a4f221a483203501e4522a08019", 1000),
                ("krytoy", "65e84be33532fb784c48129675f9eff3a682b27168c0ea744b2cf58ee02337c5", 1000);'''

fill_bets = '''INSERT INTO bets (user_id, bet_amount) VALUES 
                (2, 500),
                (4, 200), 
                (3, 1000),
                (1, 123);'''

fill_betsevents = '''INSERT INTO betsevents (bets_id, event_id) VALUES
                    (1, 2),
                    (3, 1),
                    (4, 5),
                    (2, 3);'''

with sqlite3.connect("coursework.db") as connection:
    cursor = connection.cursor()
    cursor.execute(fill_sports)
    cursor.execute(fill_teams)
    cursor.execute(fill_events)
    cursor.execute(fill_users)
    cursor.execute(fill_bets)
    cursor.execute(fill_betsevents)
    connection.commit()
print("Done!")