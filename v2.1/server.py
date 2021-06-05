# -*- coding: cp949 -*- 

import pandas as pd
import pymysql
import paramiko

class SQL():
    def receive(self, uid):
        sql = "SELECT * FROM bus_info"
        self.cursor.execute(sql)
        self.result = self.cursor.fetchall()
        self.df = pd.DataFrame(self.result)
        self.bus_info = self.df[self.df['bus_uid'] == uid]
        self.db.commit()

    def connect(self):
        host = "34.64.183.238"
        username = 'uosmooyaho'
        try:
            self.db = pymysql.connect(
                user = 'uosmooyaho',
                passwd = '!Andigh123',
                host = "34.64.183.238",
                database = "bus_info"
            )
            self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # need to modify keyfilename
            self.ssh.connect(host, username='moyahoo', key_filename='C:\\Users\\bbiuy\\Documents\\1_Workspace\\python\\bus_driver\\myh_keyfile.pem')
            self.sftp = self.ssh.open_sftp()
            print("sftp connect success")
        except:
            print("Connect Error")
            return False
        finally:
            pass

    def receive_img(self, bus_id):
        filename = 'fall_detected.jpg'
        self.sftp.listdir()
        with open('image\\'+filename, 'wb') as contents:
            self.sftp.chdir('/home/moyahoo//fall_detection')
            self.sftp.get(str(bus_id)+'.jpg', 'C:\\Users\\bbiuy\\Documents\\1_Workspace\\python\\bus_driver\\image\\'+filename)
            contents.close()

    def down_fall_sig(self, bus_id):
        try:
            sql = '''UPDATE `bus_info`
                    SET fall_sig = '0'
                    WHERE bus_uid = '%s';'''
            self.cursor.execute(sql, bus_id)
            self.db.commit()
        except:
            print("Connect Error")

if __name__ == '__main__':
    c = SQL()
    c.connect()
    c.receive_img(105000102)