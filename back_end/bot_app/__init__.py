from flask import Flask
import bot_app.fulfillment.utility as util
from bot_app.fulfillment.controllers import fulfillment

app = Flask(__name__)

app.config.from_object('config')

app.register_blueprint(fulfillment)

util.init_app(app)

@app.route('/')
def index():
    return 'Service Working!!!'

@app.route('/test')
def test():
    return util.simple_response('Hello World Test!!')