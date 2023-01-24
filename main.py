from flask import Flask
from flask_restx import Api
from views.bets import bets_ns
from views.my_bets import my_bets_ns
from views.utils import utils_ns
from views.log_in import log_in_ns
from views.sign_up import sign_up_ns
from views.teams import team_ns

def create_app():
    app = Flask(__name__)
    return app

def configure_app(app):
    api = Api(app) 
    api.add_namespace(bets_ns)
    api.add_namespace(my_bets_ns)
    api.add_namespace(utils_ns)
    api.add_namespace(log_in_ns)
    api.add_namespace(sign_up_ns)
    api.add_namespace(team_ns)

if __name__ == "__main__":
    app = create_app()
    configure_app(app)
    app.run(debug=True, host='0.0.0.0')