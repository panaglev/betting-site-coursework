import os
import sys
import jwt
import requests

SECRET = "etg64vtah7r6atw74afiar6jtw4rsetrset69c8s"

chelyad_greeting = """Please enter what do you want to do:
1. List all available bets
2. Make a bet
3. See bets history
4. See my bets
0. Exit"""

moderator_greeting = """Please enter what do you want to do:
1. List all available bets
2. Make a bet
3. See bets history
4. See my bets
5. Moderate users
6. Create event
0. Exit"""

admin_greeting = """Let us make your wish come true
1. List all available bets
2. Make a bet
3. See bets history
4. See all my bets
5. Moderate users
6. Create event
7. Make a payback
0. Exit"""

def main():
    flag = True
    choise = int(input("""Hello, before we can keep our dirty deals we've gotta to authorize.
1. Authorize
2. Register
0. Exit """))
    token = ""
    match choise:
        case 1:
            login = input("Enter login: ")
            password = input("Enter password: ")
            credentials = {
                'login': login,
                'password': password,
            }
            r = requests.post('http://127.0.0.1:5000/log-in', json=credentials)
            token = r.cookies.get_dict()['token']
        case 2:
            print("oh, sweety, it's ur first time, then i need to find some out about you")
            login = input("Enter login: ")
            password = input("Enter password: ")
            credentials = {
                'login': login,
                'password': password,
            }
            r = requests.post('http://127.0.0.1:5000/sign-up', json=credentials)
            token = r.cookies.get_dict()['token']
        case 0:
            sys.exit()

    data = jwt.decode(token, SECRET, "HS256")
    if data['login'] == 'Admin':
        print(f"Welcome back {data['login']}")
        while flag:
            print(admin_greeting)
            select = int(input("Make your choise lord: "))
            match select:
                case 1:
                    list_bets(token)
                case 2:
                    make_a_bet(token)
                    pass
                case 3:
                    see_bets_history()
                case 4:
                    list_my_bets(token)
                case 5:
                    moderate_users(token)
                case 6:
                    create_event(token)
                case 7:
                    make_payback(token)
                case 0:
                    sys.exit()
    elif data['login'] in ("Vasya_Mask_of_Madness", "Stalker_1337"):
        print(f"Welcome back {data['login']}")
        while flag:
            print(moderator_greeting)
            select = int(input("Make your choise buddy: "))
            match select:
                case 1:
                    list_bets(token)
                case 2:
                    make_a_bet(token)
                case 3:
                    see_bets_history()
                case 4:
                    list_my_bets(token)
                case 5:
                    moderate_users(token)
                case 6:
                    create_event(token)
                case 0:
                    sys.exit()
    else:
        print(f"Welcome back {data['login']}")
        while flag:
            print(chelyad_greeting)
            select = int(input("Make your choise: "))
            match select:
                case 1:
                    list_bets(token)
                case 2:
                    make_a_bet(token) 
                case 3:
                    see_bets_history()
                case 4:
                    list_my_bets(token)
                case 0:
                    sys.exit()

def list_bets(token):
    """List all available bets"""
    cookie = {"token":token}
    r = requests.get('http://127.0.0.1:5000/bets', cookies=cookie)
    print(r.json())

def make_a_bet(token):
    """Make a bet on event"""
    event_id = int(input("Enter number of event where you want to make a bet: "))
    assume_win = int(input("Who do you think is gonna win(number): "))
    bet_amount = int(input("How much money do you want to bet: "))
    bet_info = {
                'event_id':event_id,
                'assume_win':assume_win,
                'bet_amount':bet_amount,
                }
    cookie = {"token":token}
    r = requests.post("http://127.0.0.1:5000/bets", json=bet_info, cookies=cookie)
    print(r.json())

def see_bets_history():
    """See events history"""
    r = requests.get("http://127.0.0.1:5000/bets/history")
    print(r.json())

def list_my_bets(token):
    """List all my bets"""
    select = int(input("""1. See active bets \n2. See paid bets"""))
    match select:
        case 1:
            cookie = {"token":token}
            r = requests.get("http://127.0.0.1:5000/my-bets/active", cookies=cookie)
            print(r.json())
        case 2:
            cookie = {"token":token}
            r = requests.get("http://127.0.0.1:5000/my-bets/paid", cookies=cookie)
            print(r.json())

def moderate_users(token):
    select = int(input("""1. List users
             2. Change users balance"""))
    match select:
        case 1:
            cookie = {"token":token}
            r = requests.get("http://127.0.0.1:5000/utils/users", cookies=cookie)
            print(r.text)
        case 2:
            cookie = {"token":token}
            balance = int(input("Enter new users balance: ")) 
            data = {"balance": balance}
            r = requests.patch("http://127.0.0.1:5000/utils/users")
    print(r.json())

def create_event(token):
    cookie = {"token":token}
    r = requests.get("http:127.0.0.1:5000/teams", cookies=cookie)
    print(r.json())
    team1_id = int(input("Enter team 1 id"))
    team2_id = int(input("Enter team 2 id"))
    data = {"team1_id": team1_id, "team2_id": team2_id}
    r = requests.post("http:127.0.0.1:5000/utils/events", json=data, cookies=cookie)
    print(r.json())

def make_payback(token):
    cookie = {"token":token}
    r = requests.get("http:127.0.0.1:5000/teams", cookies=cookie)
    event_id = int(input("Enter event id: "))
    winner = int(input("Enter winner(1/2): "))
    data = {"event_id":event_id, "winner":winner}
    r = requests.post("http:127.0.0.1:5000/utils/payback", json=data, cookies=cookie)

if __name__ == "__main__":
    main()