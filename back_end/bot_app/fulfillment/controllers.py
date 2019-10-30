import os
import bot_app.fulfillment.utility as util
import bot_app.fulfillment.buying_drink as buying_drink
import bot_app.fulfillment.system_pic as system_pic
import bot_app.fulfillment.whl_family as whl_family
import bot_app.fulfillment.whl_report as whl_report
from flask import Blueprint, Flask, jsonify, request, json
import threading
import time
import requests
from queue import Queue

# app = Flask(__name__)
fulfillment = Blueprint('fulfillment', __name__, url_prefix='/qa_bot/fulfillment')

result = None


@fulfillment.route('', methods=['GET', 'POST'])
def index():
    jsonObj = request.get_json()
    try:
        handleName = jsonObj.get('queryResult').get('intent')['displayName']
        print('Handler:', handleName)

        return eval(handleName + '(jsonObj)')
    except Exception as e:
        print(str(e))
        return util.simple_response(fulfillmentObj=util.reset_all_contexts(fulfillmentObj=jsonObj))
        # return util.simple_response(str(e))


@fulfillment.route("/short_call", methods=['GET', 'POST'])
def five_secend_call():
    global result
    result = None
    curr = time.time()
    thread = threading.Thread(target=fetch_url, name='query_qa_thread')
    thread.start()
    while (curr + 4.5) > time.time():
        if not result == None:
            return jsonify(result.json())
        else:
            time.sleep(0.3)
    return jsonify({"respone": "None"})


def fetch_url():
    global result
    my_headers = {'Authorization': 'EndpointKey 365cdd9c-7af2-48bd-9dfe-031986319115',
                  'Content-Type': 'application/json'}
    res = requests.post(
        'https://whlqakb.azurewebsites.net/qnamaker/knowledgebases/f15e1174-339e-4a81-a95e-747143f77b02/generateAnswer'
        , headers=my_headers
        , json={"question": "outlook有問題可以找誰?"})
    print(res.json())
    result = res
    return res

def init_app(app):
    app.register_blueprint(fulfillment)
    util.init_app(app)
    buying_drink.init_app(app)
    system_pic.init_app(app)
    whl_report.init_app(app)
    whl_family.init_app(app)