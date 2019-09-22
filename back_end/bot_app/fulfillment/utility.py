
from flask import jsonify
def simple_response(text_content='', fulfillmentObj=None):
    if not fulfillmentObj==None:
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

def lookup_context(fulfillment,lookup_pattern):
    contexts = fulfillment.get('queryResult').get('outputContexts')
    search_key = fulfillment.get('session') + '/contexts/' + lookup_pattern
    return next((x for x in contexts if x['name']== search_key),None)