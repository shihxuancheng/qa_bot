# %%
import requests
from bs4 import BeautifulSoup as bs

base_url = 'http://family.wanhai.com'
loginURL = base_url + '/Login.jsp'
account = 'M1933'
password = 'Whlm1933'
payload = {'Account': account, 'Password': password}
meeting_rooms = None
massage_rooms = None
session_req = None


# session_req.post(loginURL,data=payload)

# %%
def login(id, pw):
    global session_req
    if session_req is None:
        session_req = requests.Session()
    res = session_req.post(
        loginURL, data={'Account': account, 'Password': password})
    print(res.request.headers['Cookie'])


# %%
def isLogin():
    global session_req
    if session_req is None:
        session_req = requests.Session()
    route_url = base_url + '/MainPage.jsp'
    res = session_req.get(route_url, allow_redirects=False)
    if res.status_code == 200:
        print(res.request.headers['Cookie'])
        return True
    else:
        return False


# %%
def getEquipList(type='MEETING'):
    equipList_url = base_url + '/LeaseEquip/equipListOnePage.jsp'
    result = session_req.get(
        equipList_url + '?file_num=61621&account_id=' + account + '&equip_type=' + type)
    print(result.request.headers['Cookie'])

    soup = bs(result.text, 'html.parser')
    elements = soup.find_all('input', {'id': 'check2', 'name': 'ID_keyD'})
    equipDict = dict()
    for v1, v2 in [(e['value'], e.find_parent().find_next_sibling().text) for e in elements]:
        equipDict[v1] = {'id': v1, 'type': type, 'name': v2}
    # print(equipDict)
    return equipDict


# %%
def getEquipName(equipId):
    if equipId in meeting_rooms.keys():
        return meeting_rooms[equipId]['name']
    elif equipId in massage_rooms.keys():
        return massage_rooms[equipId]['name']
    else:
        return None


# %%
# 查詢設備是否已被占用(by 特定日期/時段)
def isEquipInUsed(b_date, b_time, e_time, equip_type, equip_id):
    if equip_type == 'MASSAGE':
        print('Not Support Now!!!')
        return False
    equipUsageURL = base_url + '/LeaseEquip/equipUsage.jsp'
    payload = [('q_from_date', b_date),
               ('q_from_time', b_time),
               ('q_to_date', b_date),
               ('q_to_time', e_time),
               ('q_equip_type', equip_type),
               ('ID_keyD', equip_id)]
    result = session_req.post(equipUsageURL, data=payload)
    soup = bs(result.text, 'html.parser')
    elements = soup.select('td > b')
    if (len(elements) > 1) and (not '目前無人預約' in elements[1].text):
        return True
    else:
        return False
    return False


# %%
# 查詢設備可用時段(by 特定日期
def search_available_time(equip_type, equip_id, strDate):
    if equip_type == 'MASSAGE':
        print('Not Support Now!!!')
        return
    from interval import Interval
    equipUsageURL = base_url + '/LeaseEquip/equipUsage.jsp'
    payload = [('q_from_date', strDate),
               ('q_from_time', ''),
               ('q_to_date', strDate),
               ('q_to_time', ''),
               ('q_equip_type', equip_type),
               ('ID_keyD', equip_id)]
    result = session_req.post(equipUsageURL, data=payload)
    soup = bs(result.text, 'html.parser')
    # print(soup.prettify())
    print('{}:\n{}'.format(equip_id, soup.select('td[nowrap]')[0].text))


# %%
# 查詢可用設備(by 特定日期/時段)
def search_available_equips(equip_type, strDate, b_time, e_time):
    if equip_type == 'MASSAGE':
        print('Not Support Now!!!')
        return
    from interval import Interval
    equipUsageURL = base_url + '/LeaseEquip/equipUsage.jsp'
    payload = [('q_from_date', strDate),
               ('q_from_time', ''),
               ('q_to_date', strDate),
               ('q_to_time', ''),
               ('q_equip_type', equip_type)]

    payload.extend([('ID_keyD', e) for e in meeting_rooms.keys()])
    result = session_req.post(equipUsageURL, data=payload)
    soup = bs(result.text, 'html.parser')
    equips = [equip.text.strip() for equip in soup.select(
        'div[id="equips"] td[align="center"]')]
    # print(equips)
    availList = list()
    for index, elem in enumerate(soup.select('td[nowrap]')):
        availList.insert(index, 1)
        if '目前無人預約' in elem.text:
            continue
        target = Interval(int(b_time), int(e_time), closed=False)
        periods = [x.text.split('~') for x in elem.select('b')]
        periodIntvs = [Interval(x[0], x[1]) for x in list(
            map(lambda bb: [int(x) for x in bb], periods))]

        # print(equips[index])
        # for pp in periodIntvs:
        #     print(pp,'\n')

        for periodIntv in periodIntvs:
            if target.overlaps(periodIntv):
                availList[index] = 0
                break

    # print(availList)
    for index, avail in enumerate(availList):
        if avail == 1:
            print('{}\n'.format(equips[index]))


# %%
# 預約設備
def bookingEquip(equip_id, equip_type, strDate, b_time, e_time):
    if equip_type == 'MASSAGE':
        print('Not Support Now!!!')
    bookingURL = base_url + '/LeaseEquip/equipBooking_db.jsp'
    payload = {
        'item_choice1': 'F',
        'equipment_id1': equip_id,
        'lease_action1': 'book',
        'str_yymmdd': strDate,
        'f_rent_fm1': b_time,
        'f_rent_to1': e_time,
        'equip_count': '1',
        'f_str_remark1': '#7253',
        'contactor_mail1': 'x'
        # 'lease_time_code_1': '',
        # 'term_time_code1': '',
        # 'equip_name_c1': '<5F>台北廳 【可容納90人】',
        # 'lease_time_code1': 'enter_rent_time',
        # 'tea1': '0',
        # 'water1': '0',
        # 'coffee1': '0',
        # 'meeting_type1': 'IN',
        # 'selected_year': '2019',
        # 'selected_month': '06',
        # 'selected_day': '06',
        # 'equip_type': 'MEETING',
        # 'fm_date': '20190606',
        # 'to_date': '20190606',
        # 'select_equips': equip_id
    }
    soup = bs(session_req.post(bookingURL, data=payload).text, 'html.parser')
    print(soup.select('table tr:nth-child(2) td:nth-child(5)')[0].text)
    # print(soup.prettify())


# %%
# 取消預約設備
def cancalBookingEquip(equip_type, rent_no):
    if equip_type == 'MASSAGE':
        print('Not Support Now!!!')
    bookingURL = base_url + '/LeaseEquip/userBooking_db.jsp'
    payload = {
        # 'ID_key': '0u',
        # 'action_type_0u': 'U',
        'action_type': 'D',
        'ID_keyDD': rent_no,
        # 'i_rent_no_0u': rent_no
        # 'ID_key': '1u',
        # 'action_type_1u': 'U',
        # 'i_rent_no_1u': '350438',
        # 'q_equip_id':'',
        # 'q_rent_date':'',
        # 'q_rent_no':'',
        # 'q_su_id':''
    }
    soup = bs(session_req.post(bookingURL, data=payload).text, 'html.parser')
    print(soup.prettify())


# %%
# 列出個人設備預約紀錄
def listRentedEquips():
    equipList_url = base_url + '/LeaseEquip/equipListOnePage.jsp'
    result = session_req.get(
        equipList_url + '?file_num=61621&account_id=' + account + '&equip_type=MEETING')
    soup = bs(result.text, 'html.parser')
    elements = soup.select('form[name="dataForm1"] input[name^="i_rent_no"]')
    elements = [x.find_parent().select('td[align="center"]') for x in elements]
    rentedList = [(x[0].input['value'], x[1].text, x[2].text, x[3].text)
                  for x in elements]
    return rentedList


# %%
# listRentedEquips()

# %%
# equipId = 'CF15-10F-DN-01'
# print(getEquipName(equipId))
# inUsed = isEquipInUsed('20190606', '1900', '2000', 'MEETING', equipId)
# print('Equip in used? {}'.format(inUsed))
# %%
# search_available_equips('MEETING', '20190624', '0900', '1200')
# %%
# search_available_time('MEETING', 'CF01-9F', '20190624')

# %%
# if not isLogin():
#     login(account, password)
# meeting_rooms = getEquipList('MEETING')
# massage_rooms = getEquipList('MASSAGE')
#
# for x in meeting_rooms:
#     print(x, meeting_rooms.get(x))
# print('\n')
# for x in massage_rooms:
#     print(x, massage_rooms.get(x))

# %%
if __name__ == '__main__':
    pass
