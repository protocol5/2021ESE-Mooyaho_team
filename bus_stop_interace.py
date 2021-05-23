from os import read
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
import requests, xmltodict, json
import threading
import csv 
import pymysql

##DB 접속
db = pymysql.connect(
    user = 'kyukk7',
    passwd = 'andigh',
    host = "34.64.138.186",
    database = "bus_info"
)

# 버스 정류장 API 인증 key
bus_stop_key = "YCw62AJ77rUCLVLmI%2BrkReS65%2F5H4XavS%2BIVCLqjeDLq9MaS9v2BkixjD1xgDBvFG%2F6MvUlcmJ44d1PGxruD4A%3D%3D"
# 버스 도착정보 조회 API 인증 key
# key = "YCw62AJ77rUCLVLmI%2BrkReS65%2F5H4XavS%2BIVCLqjeDLq9MaS9v2BkixjD1xgDBvFG%2F6MvUlcmJ44d1PGxruD4A%3D%3D"
key = "gHcpum2l%2Bw3H75tj8jtT%2BsZ7MSiSpkzn1FlH0mpM4meW1yoDcQmtZv0T5XiDOYXqV5kGvwVi5Rdu7p%2FiJBuezg%3D%3D"


# 버스 정보 받아오는 부분
# 버스 정류장 고유의 id 입력
busstop_id = 105000102

url = "http://ws.bus.go.kr/api/rest/arrive/getLowArrInfoByStId?ServiceKey={}&stId={}".format(key, busstop_id)
content = requests.get(url).content
dict = xmltodict.parse(content)
jsonString = json.dumps(dict['ServiceResult']['msgBody'], ensure_ascii=False)
jsonObj = json.loads(jsonString)


bus = []  # 버스 번호와 도착 예정 시간이 순차적으로 담김
bus_number_array = []
num_of_bus = 0
bus_time_array = []
#####################################################

# 세마포어
sem = threading.Semaphore(1)

init_class = 0  # 쓰레드 2에서 처음에만 실행하려고

for i, item in enumerate(jsonObj['itemList']):
    print(item['rtNm'], item['arrmsg1'])

    bus.append(item['rtNm'])
    # bus_number_array[i] = item['rtNm']
    bus_time_array.append(item['arrmsg1'])
    bus_number_array.append(item['rtNm'])

print(bus_number_array)
num_of_bus = len(bus_number_array)

print('check bus: {} {}'.format(bus[0], bus[1]))

current_page = 0  # 맨 처음 페이지
BUS_NUMBER = len(bus_number_array)  # 버스의 수
MAX_PAGE = len(bus_number_array) // 10  # 최대 페이지
FLAGS = [1] * len(bus_number_array)  # 1이면 버스 버튼을 누를 수 있는 상태

if (len(bus_number_array) % 10 == 0):
    MAX_PAGE -= 1

# seg fault를 방지하기위해 10단위로 빈칸을 채워넣음
if MAX_PAGE == 0:
    while (len(bus_number_array) < 10):
        bus_number_array.append('')


f = open('bus_route_id.csv', 'r', encoding='UTF-8')
rdr = csv.reader(f)
bus_id = [] # 해당 정류장에 도착하는 버스의 고유 id가 담길 배열
for line in rdr :
    if line[0] in bus:
        bus_id.append(line[1])
print('array', bus_id)
f.close()



################### xml 파일을 읽어와서 버스 정류장을 ui에 표시
bus_stop_id = [] # 버스 정류장의 id, ars, name
bus_stop_ars = [''] * 5 
bus_stop_name = [''] * 5

with open('bus_stop.xml') as fd_xml:
    dict_1 = xmltodict.parse(fd_xml.read())
    jsonString_1 = json.dumps(dict_1['bus_stop'], ensure_ascii=False)
    jsonObj_1 = json.loads(jsonString_1)

for i, item in enumerate(jsonObj_1['bus_stop_id']):
    if item['bus_stop_name'] == str(busstop_id):
        bus_stop_id.append(item['bus_stop_1'])
        bus_stop_id.append(item['bus_stop_2'])
        bus_stop_id.append(item['bus_stop_3'])
        bus_stop_id.append(item['bus_stop_4'])
        bus_stop_id.append(item['bus_stop_5'])

read_id_csv = open('bus_stop_id.csv','r',encoding='euc-kr')
read_id = csv.reader(read_id_csv)

for i, line in enumerate(read_id):
    if line[0] in bus_stop_id :
        index = 0
        for j in range(5):
            if bus_stop_id[j] == line[0]:
                index = j
                bus_stop_ars[index] = line[1]
                bus_stop_name[index] = line[2]
                break
            else :
                index +=1
print(bus_stop_id)
print(bus_stop_ars)
print(bus_stop_name)

read_id_csv.close()

# 버스 도착 시간을 계속 받아오기 위한 쓰레드
class Thread1(threading.Thread):
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        while (1):
            content = requests.get(url).content
            dict = xmltodict.parse(content)
            jsonString = json.dumps(dict['ServiceResult']['msgBody'], ensure_ascii=False)
            jsonObj= json.loads(jsonString)

            for i,item in enumerate(jsonObj['itemList']):
                if (bus_time_array[i] != item['arrmsg1'] and bus_time_array[i]=='곧 도착'):
                    print(bus[i]+'번 버스가 도착했다가 떠났읍니다.')

                if (bus_time_array[i] == '운행종료') :
                    sem.acquire()
                    FLAGS[i] = 0
                    sem.release()
                # 버스가 정류장에 도착했다가 떠났을 때. 
                if (FLAGS[i] == 0 and bus_time_array[i] != item['arrmsg1'] and bus_time_array[i]=='곧 도착' ) :
                    print('{}번 버스 다시 누를 수 있게 해야함'.format(bus[i]))
                    sem.acquire()
                    FLAGS[i] = 2
                    sem.release()
                bus_time_array[i] = item['arrmsg1']
            print(bus)
            print(bus_time_array)
            # WindowClass.bus_button(self)##############################여기부터
            time.sleep(10)




class QtGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("버스 지유아이")
        self.resize(1280, 800)

        # but_list 배열에는 버튼들이 담긴다.
        self.but_list = []
        # 이 배열에는 버스 정류장 버튼들이 담긴다.
        self.but_stop_list = []
        # 이 배열에는 이전 다음 버튼이 담긴다
        self.previous_next_list = []



        # 버스 도착정보 받아오는 쓰레드
        thread1 = Thread1()
        thread1.start()

        # 버스 관련 버튼 생성
        self.make_previous_button()
        self.make_next_button()
        for i, num in enumerate(bus_number_array):
            self.make_bus_button(num, i)

        # 정류장 관련 버튼생성
        for i in range(5):
            self.make_bus_stop_button(i)


        # refresh.py 에서 따온 것
        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.Refresh)

        self.time.start()


        # self.show()

    def Refresh(self):
        # print('Refresh')
        global FLAGS , num_of_bus


        for i in range(num_of_bus):
            sem.acquire()
            if FLAGS[i] == 2 :
                self.but_list[i].setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")
                # print(self.but_list[i].isEnabled())
                self.but_list[i].setEnabled(True)
                FLAGS[i] = 1
                self.connect_db(bus_number_array[i] ,0)

            elif FLAGS[i] == 0 :
                self.but_list[i].setStyleSheet("background-image : url(bus_il4.png); Text-align:top; font-size:40pt; font : Roman")
                # print(self.but_list[i].isEnabled())
                self.but_list[i].setEnabled(False)
            sem.release()


        print(FLAGS)
        # self.time.stop()




    #버스 클릭 버튼을 만드는 함수
    def make_bus_button(self, bus_number, i):
        button = QPushButton(str(bus_number), self)
        # button.setEnabled(True)
        button.resize(280, 120)
        button.setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")

        w = 0
        v = 0

        if i < 5 :
            w = 10
            v = i

        else :
            w = 300
            v = i -5

        button.move(w, v*130+30)
        self.but_list.append(button)

        # print(self.but_list)

        if button.text() == '':
            button.setEnabled(False)

        button.clicked.connect(lambda: self.click_bus_num(button))


    # 버스 정류장 버튼을 만드는 함수
    def make_bus_stop_button(self,i):
        button = QPushButton(bus_stop_name[i],self)
        button.resize(600,120)
        button.setStyleSheet("Text-align:center; font-size:30pt; font : Roman")

        w = 620
        v = 100
        v = i * 140 + 50

        button.move(w,v)

        self.but_stop_list.append(button)

        button.clicked.connect(lambda: self.click_bus_stop_button(button))

    #이전 버튼 만드는 함수
    def make_previous_button(self):
        global MAX_PAGE

        button = QPushButton('이전', self)
        button.resize(280, 80)
        button.move(10, 680)
        button.setStyleSheet(" font-size:40pt; font : Roman")
        self.previous_next_list.append(button)
        button.clicked.connect(lambda : self.click_previous_button())

        # if MAX_PAGE == 0 :
        #     button.setEnabled(False)

    def click_previous_button(self):
        print('이전 버튼이 클릭되었습니다')

    def make_next_button(self):
        global MAX_PAGE

        button = QPushButton('다음', self)
        button.resize(280, 80)
        button.move(300, 680)
        button.setStyleSheet(" font-size:40pt; font : Roman")
        self.previous_next_list.append(button)
        button.clicked.connect(lambda : self.click_next_button())

        # 버스 수에 따라 버튼 활성화 및 비활성화
        # if MAX_PAGE == 0 :
        #     button.setEnabled(False)

    def click_next_button(self):
        print('다음 버튼이 클릭되었습니다')




    def click_bus_num(self, button):
        print('Bus number', button.text(), 'is pushed!!')
        
        # 팝업 메세지 박스
        messagebox = TimerMessageBox1(button.text(), 0.5, self)
        messagebox.exec_()
        button.setEnabled(False)
        button.setStyleSheet("background-image : url(bus_il4.png); Text-align:top; font-size:40pt; font : Roman")

        for i,number in enumerate(bus_number_array) :
            if number == button.text():
                # print(type(number), type(button.text()))
                sem.acquire()
                FLAGS[i] = 0
                sem.release()
                print('버스번호 {}는 선택할 수 없습니다.'.format(button.text()))
                break


        self.connect_db(button.text(), 1)
        
    # def refresh_button(self, button):
    #     # for i in self.but_list:
    #     #     i.setEnabled(True)
    #     # self.but_list[0].setEnabled(True)

    def click_bus_stop_button(self, button) :
        global bus_id
        global busstop_id # 지금 버스 정류장의 번호
        print(button.text() + "정류장이 선택되었습니다.")
        #button.setEnabled(False)
        

        able_bus_list = [] # 현재 정류장에서 목표 정류장까지 도달할 수 있는 버스의 목록이 담김
        index_but = 0

        for i in range(5):
            if button.text() == bus_stop_name[i]:
                index_but = i 
                break

        # 공공 api를 이용해서 이용자가 가고자하는 버스 정류장에 도착하는지 여부 출력
        for bus_bus in bus_id :
            url = "http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?serviceKey={}&busRouteId={}".format(bus_stop_key, bus_bus)
            content = requests.get(url).content
            dict = xmltodict.parse(content)
            jsonString = json.dumps(dict['ServiceResult']['msgBody'], ensure_ascii=False)
            jsonObj = json.loads(jsonString)
            st, ed = -1 , -1
            for i, item in enumerate(jsonObj['itemList']):
                if item['station'] == str(busstop_id):
                    st = i
                elif item['station'] == str(bus_stop_id[index_but]) :
                    ed = i
            # print('st = ',st , 'ed= ', ed)
            if ed == -1 :
                continue
            elif st>=0 and ed >=0:
                if ed > st :
                    able_bus_list.append(item['busRouteId'])
                    able_bus_list.append(item['busRouteNm'])
        print('현재 정류장에서 해당 정류장에 도착할 수 있는 버스는 다음과 같습니다')
        print('able bus list = ', able_bus_list)

        self.chose_fast_bus(able_bus_list)

    # 도착할 수 있는 버스 중 가장 빠른 버스를 골라주는 부분
    def chose_fast_bus(self, bus_list):
            content = requests.get(url).content
            dict = xmltodict.parse(content)
            jsonString = json.dumps(dict['ServiceResult']['msgBody'], ensure_ascii=False)
            jsonObj= json.loads(jsonString)

            bus_times = [''] * len(bus_list)  # 버스 도착 시간이 저장될 배열
            for i,item in enumerate(jsonObj['itemList']):
                # 갈 수 있는 버스일 때 
                if item['busRouteId'] in bus_list :
                    for j,bus in enumerate(bus_list) :
                        if item['busRouteId'] == bus:
                            bus_times[j] = item['arrmsg1']
                            bus_times[j+1] = item['rtNm']
                        
            # print('bus_times = ', bus_times)

            self.calculate_fast_bus(bus_times)

    def calculate_fast_bus(self, bus_times):
        global bus_number_array
        bus_only_time = []
        for i, data in enumerate(bus_times):
            if i % 2 == 0 :
                bus_only_time.append(data)

        print(bus_only_time)

        for i, data in enumerate(bus_only_time):
            if data == '곧 도착' :
                bus_only_time[i] = 0
            elif data == '운행종료' :
                bus_only_time[i] = 100
            elif data =='출발대기' :
                bus_only_time[i] = 99
            else :
                bus_only_time[i] = int(data.split('분')[0])

        print(bus_only_time)
        min_index = bus_only_time.index(min(bus_only_time))

        if (bus_only_time[min_index] == 100) :
            print('탑승할 수 있는 버스가 없습니다')

        else :
            print(bus_times[min_index*2+1],'을 탑승하시오')
            for i, data in enumerate(bus_number_array) :
                if data == bus_times[min_index*2+1] :
                    sem.acquire()
                    FLAGS[i] = 0
                    sem.release()
                    messagebox = TimerMessageBox2(bus_times[min_index*2+1], 1 , self)
                    messagebox.exec_()

        self.connect_db(bus_times[min_index*2+1] , 1)

        # 경우의 수 눌려있지 않다. -> 플래그 내리고 누르면 됨 -> 탑승할 버스 넘버 팝업
        # 눌려있다 -> 탑승할 버스 넘버 팝업
        # 없다 -> 없다는 메시지 팝업

    def connect_db(self, bus_route_id, flag ):
        
        read_bus = open('bus_route_id.csv','r')
        rdr_bus = csv.reader(read_bus)
        for i, line in enumerate(rdr_bus) :
            if line[0] == bus_route_id:
                bus_route_id = line[1]

        bus_route_id = 1010 ###################이 부분을 바꾸어야합니다.

        if flag == 1 :
            cursor = db.cursor(pymysql.cursors.DictCursor)
            sql = '''UPDATE bus_info 
                SET stop_sig = '1'
                WHERE bus_uid=%s AND stop_sig = '0';'''
            cursor.execute(sql,(bus_route_id))
            db.commit()

        # 승하차 신호를 0으로 바꿈
        elif flag == 0 :
            cursor = db.cursor(pymysql.cursors.DictCursor)
            sql = '''UPDATE bus_info 
                SET stop_sig = '0'
                WHERE bus_uid=%s AND stop_sig = '1';'''
            cursor.execute(sql,(bus_route_id))
            db.commit()

# 버스 번호 클릭시 팝업 생성 후 자동으로 닫히는 코드
class TimerMessageBox1(QMessageBox):
    def __init__(self, bus_number ,timeout=3, parent=None):
        super(TimerMessageBox1, self).__init__(parent)
        self.setWindowTitle("버스 선택 팝업")
        self.bus_number = bus_number
        self.time_to_wait = timeout
        self.setText("{}번 버스가 선택되었습니다 ".format(self.bus_number))
        self.setStyleSheet(" Text-align:center; font-size:20pt; font : Roman")
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        #self.setText("wait (closing automatically in {0} secondes.)".format(self.time_to_wait))
        self.setText("{}번 버스가 선택되었습니다 ".format(self.bus_number))
        self.time_to_wait
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()


# 버스 정류장 클릭시 자동으로 닫히는 코드
class TimerMessageBox2(QMessageBox):
    def __init__(self, bus_stop ,timeout=3, parent=None):
        super(TimerMessageBox2, self).__init__(parent)
        global FLAGS
        self.setWindowTitle("버스 정류장 선택 팝업")
        
        self.bus_stop = bus_stop
        self.time_to_wait = timeout
        self.setText("{} 번을 탑승하시면 됩니다 ".format(self.bus_stop))
        self.setStyleSheet(" Text-align:center; font-size:20pt; font : Roman")
        self.setStandardButtons(QMessageBox.NoButton)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def changeContent(self):
        #self.setText("wait (closing automatically in {0} secondes.)".format(self.time_to_wait))
        self.setText("{} 번을 탑승하시면 됩니다".format(self.bus_stop))
        self.resize(800,200)
        self.time_to_wait
        self.time_to_wait -= 1
        if self.time_to_wait <= 0:
            self.close()

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = QtGUI()
    ex.show()

    app.exec_()