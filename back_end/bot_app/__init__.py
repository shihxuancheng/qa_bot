from flask import Flask
from bot_app.fulfillment.controllers import fulfillment

app = Flask(__name__)

app.config.from_object('config')

app.register_blueprint(fulfillment)

@app.route('/')
def index():
    return 'Service Working!!!'