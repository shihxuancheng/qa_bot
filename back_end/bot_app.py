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

@app.route("/short_call",methods=['GET','POST'])
def five_secend_call():
    global result
    result = None
    curr = time.time()
    thread = threading.Thread(target=fetch_url,name='query_qa_thread')
    thread.start()
    while (curr + 4.5) > time.time():
        if not result == None:
            return jsonify(result.json())
        else:
            time.sleep(0.3)
    return jsonify({"respone":"None"})

def fetch_url():
    global result
    my_headers = {'Authorization': 'EndpointKey 365cdd9c-7af2-48bd-9dfe-031986319115','Content-Type':'application/json'}
    res = requests.post('https://whlqakb.azurewebsites.net/qnamaker/knowledgebases/f15e1174-339e-4a81-a95e-747143f77b02/generateAnswer'
    ,headers=my_headers
    ,json={"question":"outlook有問題可以找誰?"})
    print(res.json())
    result = res
    return res

@app.route('/qa_bot/fulfillment', methods=['GET', 'POST'])
def index():
    jsonObj = request.get_json()
    # print(type(jsonObj))
    # print(jsonObj)
    # print('responseId => {},\n session => {}'.format(jsonObj.get('responseId'),jsonObj.get('session')))
    # print(request.get_data(as_text=True))
    try:
        handleName = jsonObj.get('queryResult').get('intent')['displayName']
        print('Handler:',handleName)
        
        return eval(handleName+'()')
    except:
        return sample_response('找不到對應的fulfillment handler!!!')

def buying_drink_ask_category():
    drinkCate = fulfillment.get('queryresult').get('parameters')['drink_category']
    print('Category: ',drinkCate)
    if drinkCate == '咖啡':
        return sample_response('美式、拿鐵還、卡布奇諾')
    elif drinkCate == '茶':
        return sample_response('紅茶、綠茶、烏龍茶')
    elif drinkCate == '果汁':       
        return sample_response('芒果汁、檸檬汁、芭樂汁') 
     
    return sample_response('you got it')        

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
        'source':'richard-shih.idv.tw'          
    }
    return jsonify(jsonResp)


def main():
    port = os.environ.get('FLASK_EXPOSE_PORT')
    port = port if port != None else 8080
    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
    main()
