import os
import time
import paramiko
import pymysql
import pandas as pd
from datetime import datetime
import requests, xmltodict, json

####################################################################################################
##### 함수 정의 공간 ###############################################################################
####################################################################################################
key = "w3a%2BGOTdnUnvwp6vPjq52gbKLKEHfhAyvRIZU9HIfPV%2B3JtqtiVmWwdbcfJDHNcLcyiqWrQPNqwdgnIUmv9KZA%3D%3D"
#key = "EriOCrxdGnpUPhdYrX8UCV0bzKOz3iXOHasrwbMMtYSpueHgIdKiEgK3GX4a%2Bb8TVTqjzD4Qd%2F4p4mPJPQ9nhA%3D%3D"
# fall_sig 일부만 수정
def update_fall_sig_partial(fall_sig, bus_uid):
    sql = '''UPDATE `bus_info`
      SET fall_sig = %s
      WHERE bus_uid = %s ;'''
    cursor.execute(sql, (fall_sig, bus_uid))
    mydb.commit()


# 전체 수정
def update_fall_sig_all(fall_sig):
    sql = '''UPDATE `bus_info`
      SET fall_sig = %s;'''
    cursor.execute(sql, (fall_sig))
    mydb.commit()


# db에 행 추가하기
def Insert(list_no, bus_num, bus_uid, stop_sig, fall_sig, input_date):
    sql = '''INSERT INTO bus_info(list_no, bus_num, bus_uid, stop_sig, fall_sig, input_date)
        VALUES (%s, %s, %s, %s, %s, %s);'''
    cursor.execute(sql, (list_no, bus_num, bus_uid, stop_sig, fall_sig, input_date))
    mydb.commit()


# db에 행 삭제하기
def Delete(list_no):
    sql = '''DELETE FROM `bus_info`
        WHERE list_no = %s;'''
    cursor.execute(sql, (list_no))
    mydb.commit()
    
    
# 버스 목록 중 곧 도착이 있는지 확인하기
def find_soon(jsonObj):
    for i, item in enumerate(jsonObj['itemList']):
        if item['arrmsg1'] == '곧 도착':
            return item['busRouteId']
    # 곧 도착인 버스가 아무것도 없으면 0을 리턴    
    return 0


# 버스의 도착 시간 중 가장 빠른 시간을 찾기
def find_fast_arr(jsonObj):
    for i, item in enumerate(jsonObj['itemList']):
        # 첫 번째 시간을 받은 상태라면
        if i == 0:
            arr_time = item['arrmsg1']
            bus_id = item['busRouteId']
            continue
        else:
            # 미리 담은 arr_time보다 현재 for문에서 받은 item['arrmsg1']이 더 빠를 경우 arr_time을 갱신한다.

            time1 = int(arr_time.split('분')[0])
            time2 = int(item['arrmsg1'].split('분')[0])
            if time1 >= time2:
                arr_time = item['arrmsg1']
                bus_id = item['busRouteId']
    return bus_id




####################################################################################################
##### 메인 함수 ####################################################################################
####################################################################################################
# image file path
img_file = '/home/myh/2021ESE-Mooyaho_team/darknet/fall_detected.jpg'

# get modified time of image first
modTimesinceEpoc = os.path.getmtime(img_file)
modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
print("Last Modified Time : ", modificationTime)


# keep loop for showing image (when modified time is changed)
bus_id = 0
past_bus_id = 0
count = 0
while(1):
    # get modified time again to compare
    modTimesinceEpoc_recent = os.path.getmtime(img_file)
    modificationTime_recent = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc_recent))
    print("Last Modified Time : ", modificationTime_recent)

    # if modified time is different with before time, count = 1
    if modificationTime_recent != modificationTime:
        count = 1
    # else, count = 0
    else:
        count = 0


    # if count = 1, wait 1 second for rewriting the image and imshow for 2 seconds
    # also, access db and turn on the fall_sig
    if count == 1:
        time.sleep(1)


        # Using API, 가장 빨리 도착하는 버스 찾아
        busstop_id = 105000102
        url = "http://ws.bus.go.kr/api/rest/arrive/getLowArrInfoByStId?ServiceKey={}&stId={}".format(key, busstop_id)
        content = requests.get(url).content
        dict = xmltodict.parse(content)
        jsonString = json.dumps(dict['ServiceResult']['msgBody'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)

        for i, item in enumerate(jsonObj['itemList']):
            print(item['rtNm'].center(7, ' '),' // ', item['arrmsg1'].center(20, ' '),' // ',
                '버스ID : ', item['busRouteId'].center(10, ' '))

        is_soon = find_soon(jsonObj)
        if is_soon == 0:
            print('\n곧 도착이 없습니다.\n')
            bus_id = find_fast_arr(jsonObj)
            print('가장 빠른 버스 : %s\n' %bus_id) # 곧도착이 없을 때는 find_fats_arr(jsonObj)가 버스ID이다.
        else:
            bus_id = is_soon
            print('\n곧 도착하는 버스 ID : %s\n' %bus_id) # 곧도착이 있을 때는 is_soon이 버스ID이다.


        # connect GCP with ssh
        host = '34.64.183.238'
        username = 'moyahoo'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # need to modify keyfilename@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        ssh.connect(host, username=username, key_filename='/home/myh/Desktop/myh_keyfile.pem')
        #########################################################

        # sftp open
        sftp = ssh.open_sftp()
        print("connect success")

        # file upload
        filename = 'fall_detected.jpg'
        os.chdir(r"/home/myh/2021ESE-Mooyaho_team/darknet/")
        with open(filename, 'rb') as contents:
            sftp.chdir('/home/moyahoo/fall_detection')
            sftp.put('/home/myh/2021ESE-Mooyaho_team/darknet/fall_detected.jpg', str(busstop_id)+'.jpg')
            contents.close()
        sftp.close()
        ssh.close()
        

        # db 정보 및 연결
        mydb = pymysql.connect(
            user='kyukk7', 
            passwd='andigh', 
            host='34.64.138.186', 
            db='bus_info'
        )

        # 커서 객체 생성
        cursor = mydb.cursor(pymysql.cursors.DictCursor)


        # fall_sig 수정하기 (if fastest bus_id is changed, the past bus's fall sig is dropped by 0)
        if past_bus_id != bus_id:
            update_fall_sig_partial(0, past_bus_id)
        fall_sig = 1
        update_fall_sig_partial(fall_sig, bus_id)

    # else, close the image and continue
    # also, access db and drop the fall_sig
    else:
        # db 정보 및 연결
        mydb = pymysql.connect(
            user='kyukk7', 
            passwd='andigh', 
            host='34.64.138.186', 
            db='bus_info'
        )

        # 커서 객체 생성
        cursor = mydb.cursor(pymysql.cursors.DictCursor)

        
        # fall_sig 수정하기
        fall_sig = 0
        update_fall_sig_partial(fall_sig, bus_id)
        continue

    # renewal the variable (modified time)
    modificationTime = modificationTime_recent

    # renewal past bus id
    past_bus_id = bus_id
