from flask import Flask

app = Flask(__name__)

from world_bank_app import routes
