import os
from flask import Flask, jsonify, request, json

app = Flask(__name__)


@app.route('/qa_bot/fulfillment', methods=['GET', 'POST'])
def index():
    jsonObj = request.get_json()
    # print(type(jsonObj))
    # print(jsonObj)
    print('responseId => {},\n session => {}'.format(jsonObj.get('responseId'),jsonObj.get('session')))
    print(request.get_data(as_text=True))
    return sample_response()

def sample_response():
    strRes = ''
    jsonResp = {
        'fulfillmentText':'超級帥哥Richard',
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
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    main()
