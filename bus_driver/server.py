from threading import Thread, Timer
import pandas as pd
import pymysql

class SQL():
    def receive(self, uid):
        sql = "SELECT * FROM bus_info"
        self.cursor.execute(sql)
        self.result = self.cursor.fetchall()
        self.df = pd.DataFrame(self.result)
        self.bus_info = self.df[self.df['bus_uid'] == uid]
        self.db.commit()

    def connect(self):
        try:
            self.db = pymysql.connect(
                user = 'kyukk7',
                passwd = 'andigh',
                host = "34.64.138.186",
                database = "bus_info"
            )
            self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        except:
            print("Connect Error")
            return False

    def main(self):
        # super().__init__()
        self.connect()
        self.interval_receive()

if __name__ == '__main__':
    c = SQL()