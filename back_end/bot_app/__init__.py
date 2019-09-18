from flask import Flask
import bot_app.fulfillment.utility as util
from bot_app.fulfillment.controllers import fulfillment

app = Flask(__name__)

app.config.from_object('config')

app.register_blueprint(fulfillment)

@app.route('/')
def index():
    return 'Service Working!!!'

@app.route('/test')
def test():
    return util.sample_response('Hello World Test!!')