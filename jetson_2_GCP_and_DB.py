import os
import time
import paramiko
import pymysql
import pandas as pd
from datetime import datetime

####################################################################################################
##### 함수 정의 공간 ###############################################################################
####################################################################################################
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

        # connect GCP with ssh
        host = '34.64.138.186'
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
            sftp.put('/home/myh/2021ESE-Mooyaho_team/darknet/fall_detected.jpg', 'fall_detected.jpg')
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

        # fall_sig 수정하기
        bus_uid = 1001
        fall_sig = 1
        update_fall_sig_partial(fall_sig, bus_uid)

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
        bus_uid = 1001
        fall_sig = 0
        update_fall_sig_partial(fall_sig, bus_uid)
        continue

    # renewal the variable (modified time)
    modificationTime = modificationTime_recent
