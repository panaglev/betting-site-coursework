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

fill_events = '''INSERT INTO events (team1_id, team2_id, event_status, winner) VALUES 
                (1, 6, 1, NULL),
                (2, 7, 1, NULL),
                (3, 8, 2, 1),
                (4, 9, 2, 2),
                (5, 10, 2, 2);'''

fill_users = '''INSERT INTO users (login, pass_hash, balance) VALUES 
                ("Admin", "d988fdf380f8ad79e48bd19782181ac28f59d7343009e2c16fd0054a8ddd5a38", 1000), 
                ("Kolya_Tri_Uha", "05d49692b755f99c4504b510418efeeeebfd466892540f27acf9a31a326d6504", 1000),
                ("Vasya_Mask_of_Madness", "d988fdf380f8ad79e48bd19782181ac28f59d7343009e2c16fd0054a8ddd5a38", 1000),
                ("Stalker_1337", "9bd384c77ed0641dd62109eff7ae2be206d02a4f221a483203501e4522a08019", 1000),
                ("krytoy", "35c162997f5351cbf45c8b1ddff997646189f6647c11a01d94dcec793fcd3126", 1000);'''

fill_bets = '''INSERT INTO bets (event_id, user_id, bet_amount, assume_win) VALUES
                (1, 1, 100, 1),
                (1, 2, 200, 2),
                (1, 3, 300, 2),
                (1, 4, 400, 1),
                (1, 5, 500, 1),
                (3, 1, 100, 2),
                (3, 2, 200, 1),
                (3, 3, 300, 1),
                (3, 4, 400, 2),
                (3, 5, 500, 2);'''

#fill_bets = '''INSERT INTO bets (event_id, user_id, bet_amount, assume_win) VALUES 
#                (1, 2, 500, 1),
#                (2, 4, 200, 2), 
#                (2, 3, 1000, 1),
#                (4, 1, 123, 1),
#                (4, 2, 321, 1),
#                (5, 2, 400, 2);'''


with sqlite3.connect("coursework.db") as connection:
    cursor = connection.cursor()
    cursor.execute(fill_sports)
    cursor.execute(fill_teams)
    cursor.execute(fill_events)
    cursor.execute(fill_users)
    cursor.execute(fill_bets)
    connection.commit()
print("Done!")
