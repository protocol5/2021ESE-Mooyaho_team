import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
import requests, xmltodict, json
import threading



bus_array = [10, 20, 30, 40, 50, 60 ,70 ,80 ,90, 100]

# 버스 정보 받아오는 부분

# key = "YCw62AJ77rUCLVLmI%2BrkReS65%2F5H4XavS%2BIVCLqjeDLq9MaS9v2BkixjD1xgDBvFG%2F6MvUlcmJ44d1PGxruD4A%3D%3D"
key = "gHcpum2l%2Bw3H75tj8jtT%2BsZ7MSiSpkzn1FlH0mpM4meW1yoDcQmtZv0T5XiDOYXqV5kGvwVi5Rdu7p%2FiJBuezg%3D%3D"
busstop_id = 105000103
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


iii = 0

# 버스 도착 시간을 계속 받아오기 위한 쓰레드
class Thread1(threading.Thread):
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        global iii
        while (1):
            content = requests.get(url).content
            dict = xmltodict.parse(content)
            jsonString = json.dumps(dict['ServiceResult']['msgBody'], ensure_ascii=False)
            jsonObj= json.loads(jsonString)

            for i,item in enumerate(jsonObj['itemList']):
                if (bus_time_array[i] != item['arrmsg1'] and bus_time_array[i]=='곧 도착'):
                    print(bus[i]+'번 버스가 도착했다가 떠났읍니다.')
                if (FLAGS[i] == 0 and bus_time_array[i] != item['arrmsg1'] and bus_time_array[i]=='곧 도착' ) :
                    print('{}번 버스 다시 누를 수 있게 해야함'.format(bus[i]))
                    sem.acquire()
                    FLAGS[i] = 2
                    sem.release()
                bus_time_array[i] = item['arrmsg1']
            print(bus)
            print(bus_time_array)
            bus_number_array[4] = 555
            # WindowClass.bus_button(self)##############################여기부터
            iii = iii + 1
            time.sleep(5)




class QtGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("버스 지유아이")
        self.resize(1280, 800)

        # but_list 배열에는 버튼들이 담긴다.
        self.but_list = []
        # 이 배열에는 이전 다음 버튼이 담긴다
        self.previous_next_list = []

        for i, num in enumerate(bus_number_array):
            self.make_bus_button(num, i)

        print('sesesese')

        # 버스 도착정보 받아오는 쓰레드
        thread1 = Thread1()
        thread1.start()

        self.make_previous_button()
        self.make_next_button()

        # refresh.py 에서 따온 것
        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.Refresh)

        self.time.start()


        # self.show()

    def Refresh(self):
        print('Refresh')
        global FLAGS , iii
        # self.but_list[9].setEnabled(True)
        # print(self.but_list[9].isPushed())

        # self.but_list[0].setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")
        # self.but_list[0].setEnabled(True)
        # self.but_list[0].move(800, 500)
        # print(self.but_list[0].isEnabled())
        # self.but_list[0].setEnabled(True)

        for i in range(7):
            sem.acquire()
            if FLAGS[i] == 2 :
                self.but_list[i].setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")
                # print(self.but_list[i].isEnabled())
                self.but_list[i].setEnabled(True)
                FLAGS[i] = 1
                print('j')
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

        if i ==9:
            print(self.but_list)
            # self.refresh_button(button)
            # button.update()

        button.clicked.connect(lambda: self.click_bus_num(button))
        print('button',i,button.isEnabled())


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

        ############
        # self.time.start()
        ######################

        # self.but_list = []
        # for i in range(10):
        #     self.make_bus_button(10, i)
        #     print('버튼 다시 생성', i)



    def click_bus_num(self, button):
        print('Bus number', button.text(), 'is pushed!!')
        
        # 팝업 메세지 박스
        messagebox = TimerMessageBox(button.text(), 0.5, self)
        messagebox.exec_()
        button.setEnabled(False)
        button.setStyleSheet("background-image : url(il4.jpg); Text-align:top; font-size:40pt; font : Roman")

        # self.but_list = []
        # # print(but_list)
        # for i, num in enumerate(bus_array):
        #     self.make_bus_button(10, i)
        #     print('버튼 다시 생성')

        # for bus in self.but_list:
        #     print(bus.isEnabled())
        print(type(bus_number_array[0]), type(button.text()))
        for i,number in enumerate(bus_number_array) :
            if number == button.text():
                # print(type(number), type(button.text()))
                sem.acquire()
                FLAGS[i] = 0
                sem.release()
                print('버스번호 {}는 선택할 수 없습니다.'.format(button.text()))
                break
        print('hi')
    # def refresh_button(self, button):
    #     # for i in self.but_list:
    #     #     i.setEnabled(True)
    #     # self.but_list[0].setEnabled(True)






# 버스 번호 클릭시 팝업 생성 후 자동으로 닫히는 코드
class TimerMessageBox(QMessageBox):
    def __init__(self, bus_number ,timeout=3, parent=None):
        super(TimerMessageBox, self).__init__(parent)
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



if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = QtGUI()
    ex.show()

    app.exec_()