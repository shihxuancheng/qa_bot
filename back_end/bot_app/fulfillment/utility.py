from flask import jsonify
from sqlalchemy import create_engine

db_engine = None


def simple_response(text_content='', fulfillmentObj=None):
    if not fulfillmentObj == None:
        jsonResp = fulfillmentObj
    else:
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
            'source': 'richard_shih@wanhai.com'
        }

    return jsonify(jsonResp)

def clear_response(fulfillment_obj, text_content) -> dict:
    return simple_response(fulfillmentObj={
        "fulfillmentText": text_content,
        "outputContexts": reset_all_contexts(fulfillmentObj=fulfillment_obj).get('queryResult').get(
            'outputContexts')
    })

def lookup_context(fulfillment, lookup_pattern):
    contexts = fulfillment.get('queryResult').get('outputContexts')
    search_key = fulfillment.get('session') + '/contexts/' + lookup_pattern
    return next((x for x in contexts if x['name'] == search_key), None)


# 清除所有的Output Contexts
def reset_all_contexts(fulfillmentObj=None, context_list=[]) -> dict:
    if 'queryResult' in fulfillmentObj.keys():
        contexts = fulfillmentObj.get('queryResult').get('outputContexts')
    else:
        contexts = fulfillmentObj.get('outputContexts')

    for context in contexts:
        if len(context_list) > 0:
            if context['name'] in context_list:
                context['lifespanCount'] = 0
        else:
            context['lifespanCount'] = 0

    return fulfillmentObj


def get_db_conn():
    try:
        conn = db_engine.connect()
        return conn
    except Exception as e:
        print(str(e))


def init_app(app, pre_connect=True):
    global db_engine
    db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], encoding='utf8')
    pre_connect = app.config['DATABASE_CONNECT_OPTIONS']['PRE_CONNECT']
    if pre_connect:
        try:
            conn = db_engine.connect()
        except Exception as e:
            print(str(e))
