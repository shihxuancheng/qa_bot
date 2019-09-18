import bot_app.fulfillment.utility as util
from flask import jsonify

# 確認訂單
def ordering_summary(fulfillment):
    context = util.lookup_context(fulfillment, 'buying_drink_ordering-followup')
    params = context.get('parameters')
    strResp = '您的訂購資訊如下:\n飲料: ' + params['hot_cold'] + params['drink_item.original'] + '\n數量: ' + str(params['number']) + '\n甜度冰塊: ' + params['ice_level'] + '' + params['sugar_level'] + '\n\n請問是否訂購？'
    return util.sample_response(strResp)

# 詢問飲料種類
def ask_category(fulfillment):
    params = util.lookup_context(fulfillment, 'buying_drink_dialog_context').get('parameters')

    drinks = {'咖啡': ['美式', '拿鐵', '卡布奇諾'], '茶': ['紅茶', '綠茶', '烏龍茶'], '果汁': ['芒果汁', '檸檬汁', '芭樂汁']}

    drink_cate = params.get('drink_category')
    hot_cold = params.get('hot_cold')
    drink_item = params.get('drink_item')

    response_str = '我們有'
    if not drink_item == '':
        if drink_item in sum([x for x in drinks.values()], []):
            return util.sample_response(response_str + drink_item['drink_item'])
        else:
            return util.sample_response('抱歉！我們沒有' + drink_item['drink_item'])
    else:
        if not drink_cate == '':
            return util.sample_response(response_str + ','.join(drinks.get(drink_cate)))
        else:
            return util.sample_response(response_str + ','.join(list(drinks.keys())))

    return util.sample_response('') 

# fulfillment - 訂飲料
def ordering(fulfillment):
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
def ordering_delivery_info(fulfillment):
    print(fulfillment)
    jsonRep = {
        'followupEventInput': {
            'name': 'events_order_confirm',
            'languageCode': 'zh-TW',
            'parameters': {}
        }
    }
    return jsonify(jsonRep)


