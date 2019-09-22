import bot_app.fulfillment.utility as util
'''
Intent - system_pic
'''

# 查詢系統pic
def looking_for_pic(fulfillment):
    print(fulfillment)
    sys_code = fulfillment.get('queryResult').get('parameters').get('sys_code')
    # 取得系統pic
    strRes = sys_code + '負責人是Richard Shih, Grace Liu, 請問是否幫您將問題轉達給系統負責同仁？'
    # 無法取得，請user重新輸入

    return util.simple_response(text_content=strRes)


# 確認轉達問題給pic
def confirm_forward(fulfillment):
    print(fulfillment)
    return util.simple_response(fulfillmentObj={
        'followupEventInput': {
            'name': 'events_forward_issue',
            'languageCode': 'zh-TW',
            'parameters': util.lookup_context(fulfillment, 'system_piclooking_for_pic-followup').get('parameters')
        }
    })


# 轉達問題給pic
def forward_issue(fulfillment):
    params = fulfillment.get('queryResult').get('parameters')
    employee_no = params.get('employee_no', '')
    ext_no = params.get('ext_no', '')
    issue = params.get('issue', '')
    sys_code = params.get('sys_code')

    # get user name, div, dept information from sec system by employee_no
    user_name = 'Richard Shih'

    strRes = '好的' + user_name + '已將您的問題 "' + issue + '" 轉達給 ' + sys_code + ' 負責人'
    return util.simple_response(text_content=strRes)
