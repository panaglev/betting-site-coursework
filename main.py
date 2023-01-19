from flask import Flask
from flask_restx import Api
from views.bets import bets_ns
from views.my_bets import my_bets_ns
from views.utils import utils_ns
from views.edit_bets import edit_bets_ns
from views.sign_in import sign_in_ns
from views.sign_up import sign_up_ns

def create_app():
    app = Flask(__name__)
    #HASH_SAL T= "9fc47da85894433819877a9d0e3f01f6ff35afeb25cc6058d138284abd3a050b"
    #HASH_SALT = os.environ.get('HASH_SALT') # Best practice not to save confidential information in format like above 
    return app

def configure_app(app):
    api = Api(app) 
    api.add_namespace(bets_ns)
    api.add_namespace(my_bets_ns)
    api.add_namespace(utils_ns)
    api.add_namespace(edit_bets_ns)
    api.add_namespace(sign_in_ns)
    api.add_namespace(sign_up_ns)

if __name__ == "__main__":
    app = create_app()
    configure_app(app)
    app.run(debug=True)