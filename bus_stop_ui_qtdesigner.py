import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import PyQt5
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
import requests, xmltodict, json

CalUI = uic.loadUiType('/home/dongjunego/Desktop/embed/bus_stop_ui_qtdesigner.ui')[0]

key ="YCw62AJ77rUCLVLmI%2BrkReS65%2F5H4XavS%2BIVCLqjeDLq9MaS9v2BkixjD1xgDBvFG%2F6MvUlcmJ44d1PGxruD4A%3D%3D"
busstop_id = 105000103
url = "http://ws.bus.go.kr/api/rest/arrive/getLowArrInfoByStId?ServiceKey={}&stId={}".format(key,busstop_id)

content = requests.get(url).content

dict = xmltodict.parse(content)
jsonString = json.dumps(dict['ServiceResult']['msgBody'], ensure_ascii=False)
jsonObj= json.loads(jsonString)

bus = [] #버스 번호와 도착 예정 시간이 순차적으로 담김
bus_number_array = ['']*10
num_of_bus = 0

for i,item in enumerate(jsonObj['itemList']):
    print(item['rtNm'], item['arrmsg1'])

    bus.append(item['rtNm'] )
    bus_number_array[i] = item['rtNm']
    bus.append(item['arrmsg1'] )

print(bus_number_array)
num_of_bus = len(bus_number_array)

print('check bus: {} {}'.format(bus[0],bus[1]))

class WindowClass(QMainWindow,CalUI):
    def __init__(self):
        # QDialog.__init__(self,None)
        super().__init__()
        self.setupUi(self)
        self.setMinimumSize(QSize(1280, 800))
        # uic.loadUi("/home/dongjunego/Desktop/embed/bus_stop_ui_qtdesigner.ui", self)
        print(num_of_bus)
        
        #i = 1
        #hi = exec('self.bus_number_{}'.format(i))
        #print(hi)

       #hi.setText(str(bus_number_array[0]))

        # 
        self.bus_number_1.setText(str(bus_number_array[0]))
        self.bus_number_2.setText(str(bus_number_array[1]))
        self.bus_number_3.setText(str(bus_number_array[2]))
        self.bus_number_4.setText(str(bus_number_array[3]))
        self.bus_number_5.setText(str(bus_number_array[4]))
        self.bus_number_6.setText(str(bus_number_array[5]))
        self.bus_number_7.setText(str(bus_number_array[6]))
        self.bus_number_8.setText(str(bus_number_array[7]))
        self.bus_number_9.setText(str(bus_number_array[8]))
        self.bus_number_10.setText(str(bus_number_array[9]))



        button_height , button_width = 280 , 120
        font_size = 41

        #버튼 크기 및 폰트 설정
        self.bus_number_1.setFixedSize(button_height , button_width)
        self.bus_number_1.setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")
        self.bus_number_1.setFont(QFont('Roman',font_size))
        self.bus_number_2.setFixedSize(button_height , button_width)
        self.bus_number_2.setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")
        self.bus_number_2.setFont(QFont('Roman',font_size))
        self.bus_number_3.setFixedSize(button_height , button_width)
        self.bus_number_3.setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")
        self.bus_number_3.setFont(QFont('Roman',font_size))
        self.bus_number_4.setFixedSize(button_height , button_width)
        self.bus_number_4.setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")
        self.bus_number_4.setFont(QFont('Roman',font_size))
        self.bus_number_5.setFixedSize(button_height , button_width)
        self.bus_number_5.setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")
        self.bus_number_5.setFont(QFont('Roman',font_size))

        self.bus_number_6.setFixedSize(button_height , button_width)
        self.bus_number_6.setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")
        self.bus_number_6.setFont(QFont('Roman',font_size))
        self.bus_number_7.setFixedSize(button_height , button_width)
        self.bus_number_7.setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")
        self.bus_number_7.setFont(QFont('Roman',font_size))
        self.bus_number_8.setFixedSize(button_height , button_width)
        self.bus_number_8.setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")
        self.bus_number_8.setFont(QFont('Roman',font_size))
        self.bus_number_9.setFixedSize(button_height , button_width)
        self.bus_number_9.setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")
        self.bus_number_9.setFont(QFont('Roman',font_size))
        self.bus_number_10.setFixedSize(button_height , button_width)
        self.bus_number_10.setStyleSheet("background-image : url(bus_il3.png); Text-align:top; font-size:40pt; font : Roman")
        self.bus_number_10.setFont(QFont('Roman',font_size))



        # self.bus_number_1.clicked.connect(lambda button = self.bus_number_1 : self.print_bus_number(button))
        self.bus_number_1.clicked.connect(lambda : self.print_bus_number(self.bus_number_1))
        self.bus_number_2.clicked.connect(lambda : self.print_bus_number(self.bus_number_2))
        self.bus_number_3.clicked.connect(lambda : self.print_bus_number(self.bus_number_3))
        self.bus_number_4.clicked.connect(lambda : self.print_bus_number(self.bus_number_4))
        self.bus_number_5.clicked.connect(lambda : self.print_bus_number(self.bus_number_5))
        self.bus_number_6.clicked.connect(lambda : self.print_bus_number(self.bus_number_6))
        self.bus_number_7.clicked.connect(lambda : self.print_bus_number(self.bus_number_7))
        self.bus_number_8.clicked.connect(lambda : self.print_bus_number(self.bus_number_8))
        self.bus_number_9.clicked.connect(lambda : self.print_bus_number(self.bus_number_9))
        self.bus_number_10.clicked.connect(lambda : self.print_bus_number(self.bus_number_10))



    def print_bus_number(self, button):
        
        print('Bus number  ' + button.text() +'  is pushed!!')



app = QApplication(sys.argv)
main_dialog = WindowClass()
main_dialog.show()
app.exec_()