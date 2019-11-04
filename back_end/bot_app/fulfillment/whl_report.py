import bot_app.fulfillment.utility as util


def init_app(app):
    pass


# 表列rs
def list_rs(fulfillment):
    office_code = fulfillment.get('queryResult').get('parameters').get('office_code')

    strsql = '''
    select a.rs_url,
       a.is_internet,
       decode(b.is_active, 0, 'Active', 'InActive') as status
  from was5005 a, was5011 b
 where a.office_code = :office_code
   and a.rs_id = b.rs_id
    '''

    with util.get_db_conn() as conn:
        res = conn.execute(strsql, office_code=office_code)
        res = res.fetchall()

    if len(res) == 0:
        strRes = '無法取得Office: ' + office_code + 'Report Server資訊，請重新查詢!'
        return util.clear_response(fulfillment, strRes)
    else:
        strRes = 'Office: ' + office_code + " Report Server資訊如下:\n" + ', '.join(row[0] for row in res)

    return util.simple_response(text_content=strRes)


# 取得rs資訊
def get_rs_info(fulfillment):
    office_code = fulfillment.get('queryResult').get('parameters').get('office_code')
    rs_code = fulfillment.get('queryResult').get('parameters').get('rs_code')
    rs_url = rs_code.upper() + '.WANHAI.COM:80%'
    strsql = '''select a.office_code,a.rs_url,a.is_internet,decode(b.is_active,0,'Active','InActive') as status from was5005 a,was5011 b 
    where a.rs_id=b.rs_id and upper(a.rs_url) like :rs_url and office_code like :office_code
    '''
    if office_code:
        office_code += '%'
    else:
        office_code = '%'

    with util.get_db_conn() as conn:
        res = conn.execute(strsql, rs_url=rs_url, office_code=office_code)
        res = res.fetchall()

    if len(res) == 0:
        strRes = '無法取得' + rs_code + '資訊，請重新查詢!'
        return util.clear_response(fulfillment, strRes)
    else:
        strRes = rs_code + '資訊如下:\n'
        for row in res:
            strRes += row[1] + '(office: ' + row[0] + ', isInternet: ' + row[2] + ', Status: ' + row[3] + ') '
        return util.simple_response(text_content=strRes)


# 開啟/關閉rs
def switch_on_off(fulfillment):
    office_code = fulfillment.get('queryResult').get('parameters').get('office_code')
    switch_action = fulfillment.get('queryResult').get('parameters').get('switch_action')
    rs_code = fulfillment.get('queryResult').get('parameters').get('rs_code')
    rs_url = rs_code.upper() + '.WANHAI.COM:80'
    action_code = '0' if switch_action == 'on' else '1'

    strsql = '''update was5011 set is_active=:action_code where rs_id in (select rs_id from was5005 where office_code=:office_code and upper(rs_url)=:rs_url)'''

    with util.get_db_conn() as conn:
        res = conn.execute(strsql, action_code=action_code, office_code=office_code, rs_url=rs_url)
    print(res)
    strRes = rs_code + '已' + ('開啟' if switch_action == 'on' else '關閉')
    return util.simple_response(text_content=strRes)
