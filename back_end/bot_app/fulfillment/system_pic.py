import bot_app.fulfillment.utility as util

# 查詢系統pic
def looking_for_pic(fulfillment):
    # print(fulfillment)
    sys_code = fulfillment.get('queryResult').get('parameters').get('sys_code')

    # 取得系統pic
    strsql = '''
            select *
        from (select c.user_name_e,c.user_name_c, b.user_email
                from sec1117 a, sec1118 b,sec1102 c
                where a.user_code = b.user_code
                and a.user_code=c.user_code
                and a.pic_type = 'B'
                and a.system_code = :sys_code
                order by a.pic_seq)
        where rownum <= 3
    '''
    with util.get_db_conn() as conn:
        res = conn.execute(strsql,sys_code=sys_code) 
        res = res.fetchall()
    if len(res) == 0:
       strRes = '無法取得指定系統負責人，請重新輸入'
    else:
       strRes = sys_code + '負責人是: '
       for row in res:
           strRes += row[1]+'('+row[2]+'), '
       strRes += ' 請問是否幫您將問題轉給系統負責人?'

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