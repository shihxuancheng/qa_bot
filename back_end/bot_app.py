import os
from flask import Flask, jsonify, request, json
import threading
import time
import requests
from queue import Queue

app = Flask(__name__)

result = None


@app.route('/')
def sayHi():
    return 'Hello World!!!'


@app.route("/short_call", methods=['GET', 'POST'])
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


@app.route('/qa_bot/fulfillment', methods=['GET', 'POST'])
def index():
    jsonObj = request.get_json()
    try:
        handleName = jsonObj.get('queryResult').get('intent')['displayName']
        print('Handler:', handleName)

        return eval(handleName + '(jsonObj)')
    except:
        return sample_response('找不到對應的fulfillment handler!!!')

# 確認訂單
def buying_drink_ordering_summary(fulfillment):
    context = lookup_context(fulfillment, 'buying_drink_ordering-followup')
    params = context.get('parameters')
    strResp = '您的訂購資訊如下:\n飲料: ' + params['hot_cold'] + params['drink_item.original'] + '\n數量: ' + str(params['number']) + '\n甜度冰塊: ' + params['ice_level'] + '' + params['sugar_level'] + '\n\n請問是否訂購？'
    return sample_response(strResp)

# 詢問飲料種類
def buying_drink_ask_category(fulfillment):
    params = lookup_context(fulfillment, 'buying_drink_dialog_context').get('parameters')

    drinks = {'咖啡': ['美式', '拿鐵', '卡布奇諾'], '茶': ['紅茶', '綠茶', '烏龍茶'], '果汁': ['芒果汁', '檸檬汁', '芭樂汁']}

    drink_cate = params.get('drink_category')
    hot_cold = params.get('hot_cold')
    drink_item = params.get('drink_item')

    response_str = '我們有'
    if not drink_item == '':
        if drink_item in sum([x for x in drinks.values()], []):
            return sample_response(response_str + drink_item['drink_item'])
        else:
            return sample_response('抱歉！我們沒有' + drink_item['drink_item'])
    else:
        if not drink_cate == '':
            return sample_response(response_str + ','.join(drinks.get(drink_cate)))
        else:
            return sample_response(response_str + ','.join(list(drinks.keys())))

    return sample_response('')


# fulfillment - 訂飲料
def buying_drink_ordering(fulfillment):
    params = fulfillment.get('queryResult').get('parameters')
    deliver_method = params.get('deliver_method', '')
    drink_item = params.get('drink_item.original', '')
    ice_level = params.get('ice_level', '')
    sugar_level = params.get('sugar_level', '')
    number = params.get('number', '')

    if deliver_method == '外送':
        jsonRep = {
            'followupEventInput': {
                'name': 'events_deliver_info',
                'languageCode': 'zh-TW',
                'parameters': {}
            }
        }
    else:
        jsonRep = {
            'followupEventInput': {
                'name': 'events_order_confirm',
                'languageCode': 'zh-TW',
                'parameters': {}
            }
        }
    return jsonify(jsonRep)
    # strResp = '您的訂購資訊如下:\n飲料: ' + drink_item + '\n數量: ' + str(number) + '\n甜度冰塊: ' + ice_level + '' + sugar_level + '\n\n請問是否訂購？'
    #
    # return sample_response(strResp)

# 確認地址
def buying_drink_ordering_delivery_info(fulfillment):
    print(fulfillment)
    jsonRep = {
        'followupEventInput': {
            'name': 'events_order_confirm',
            'languageCode': 'zh-TW',
            'parameters': {}
        }
    }
    return jsonify(jsonRep)


def sample_response(text_content):
    strRes = ''
    jsonResp = {
        'fulfillmentText': text_content,
        'fulfillmentMessages': [
            # {
            #     'image' : {
            #     'imageUri':'https://yt3.ggpht.com/a/AGF-l78sCrWnJHZlRs-DP1imkaINg2KkpT5Gomkahw=s900-mo-c-c0xffffffff-rj-k-no',
            #     'accessibilityText':'Hello World!!'
            #     }
            # }

            # {
            #     'card': {
            #         'title': 'card title',
            #         'subtitle': 'card text',
            #         'imageUri': 'https://assistant.google.com/static/images/molecule/Molecule-Formation-stop.png',
            #         'buttons': [
            #             {
            #                 'text': 'button text',
            #                 'postback': 'https://assistant.google.com/'
            #             }
            #         ]
            #     }
            # }
        ],
        'source': 'richard-shih.idv.tw'
    }
    return jsonify(jsonResp)


def lookup_context(fulfillment,lookup_pattern):
    contexts = fulfillment.get('queryResult').get('outputContexts')
    search_key = fulfillment.get('session') + '/contexts/' + lookup_pattern
    return next((x for x in contexts if x['name']== search_key),None)

def main():
    port = os.environ.get('FLASK_EXPOSE_PORT')
    port = port if port != None else 8080
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    main()
