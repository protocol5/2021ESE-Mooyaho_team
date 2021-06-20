# -*- coding: cp949 -*- 

import pandas as pd
import pymysql
import paramiko

class SQL():
    def num_to_uid(self,num):
        sql = "SELECT * FROM bus_info"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        df = pd.DataFrame(result)
        num = df[df['bus_num'] == str(num)]['bus_uid']
        return int(num)
        
    def receive(self, uid):
        sql = "SELECT * FROM bus_info WHERE bus_uid = '%s'"
        self.cursor.execute(sql, uid)
        self.result = self.cursor.fetchall()
        self.df = pd.DataFrame(self.result)
        self.bus_info = self.df
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
            self.ssh.connect(host, username='moyahoo', key_filename='C:\\Users\\bbiuy\\Documents\\1_Workspace\\python\\bus_driver\\myh_keyfile.pem')
            self.sftp = self.ssh.open_sftp()
        except pymysql.err.OperationalError as e:
            print("Server connect error!")
            self.connect()
        except:
            print("SSH connect error!")
            self.connect()
        else:
            print("sftp connect success")
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
    # print(c.num_to_uid(121))
    # c.receive(100100124)
    # c.receive_img(105000102)