from flask import Flask
import bot_app.fulfillment.utility as util
import bot_app.fulfillment.controllers as controller

app = Flask(__name__)

app.config.from_object('config')

controller.init_app(app)

util.init_app(app)

@app.route('/')
def index():
    return 'Service Working!!!'