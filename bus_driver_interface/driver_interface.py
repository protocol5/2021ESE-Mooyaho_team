# -*- coding: cp949 -*- 

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from threading import Timer
import time
import sys, os
import server, bus_api, line_api

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

image_width = 900
bus = '1227'
bus_No = '서울74사3540'


class BusWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.s = server.SQL()
        self.s.connect()
        self.bus_id = self.s.num_to_uid(bus)
        self.b = bus_api.API(self.bus_id, bus_No)
        self.l = line_api.API(self.bus_id)

        self.label = QLabel()
        font = QFont('Arial', 48)
        self.label.setFont(font)
        self.label.setStyleSheet("border-image: url();"
                         "border-style: solid;"
                         "border-width: 10px;"
                         "border-radius: 20px;"
                         "border-color: #004195")

        # background image 무야호
        bgimg = QImage('image\\background.jpg')
        palette = QPalette()
        palette.setBrush(10, QBrush(bgimg))
        self.setPalette(palette)

        # server 연결
        self.interval_receive()

        self.initUI()

        self.showtime()
        self.bus_receive()
 
    def initUI(self):

        self.setWindowTitle('Bus Driver Display')

        # logo box
        lbox = QHBoxLayout()
        box = QHBoxLayout()
        self.lb_logo = QLabel(self)
        self.lb_logo.setPixmap(QPixmap(QPixmap('image//logo.jpg')).scaledToHeight(140))
        self.lb_logo.setFixedSize(195,140)
        self.lb_logo.setAlignment(Qt.AlignCenter)
        box.addWidget(self.lb_logo)
        # time box
        box.addWidget(self.label)
        # 현재 상태 box
        self.lb_station = QLabel()
        self.lb_station.setText('현재: ')
        self.lb_station.setStyleSheet("color: #000000;"
                         "font: 36pt;"
                         "font: bold;"
                         "border-style: solid;"
                         "border-width: 10px;"
                         "border-radius: 20px;"
                         "border-color: #004195")
        self.lb_station.setFixedSize(900,140)
        box.addWidget(self.lb_station)
        lbox.addLayout(box)

        # image box
        imgbox = QHBoxLayout()
        box = QHBoxLayout()
        self.img_label = QLabel(self)
        self.img_label.setStyleSheet(
                        "background-image: url(image/background.jpg);"
                        "border-style: solid;"
                        "border-width: 50px;"
                        "border-color: #004195;"
                        "border-radius: 70px;"
                        )
        self.img_label.setFixedSize(1440,900)
        self.img_label.setAlignment(Qt.AlignCenter)
        box.addWidget(self.img_label, alignment=Qt.AlignCenter)
        imgbox.addLayout(box)
        vbox = QVBoxLayout()
        vbox.addLayout(lbox)
        vbox.addLayout(imgbox)

        # 버스 정보 출력
        busbox = QVBoxLayout()
        gb2 = QGroupBox()
        hbox = QHBoxLayout()
        box_st = QVBoxLayout()

        # 버스 정류장 수 출력
        self.front_st = self.stations(1)
        box_st.addWidget(self.front_st)
        self.target_st = self.stations(0)
        box_st.addWidget(self.target_st)
        self.back_st = self.stations(1)
        box_st.addWidget(self.back_st)
        hbox.addLayout(box_st)

        boxx = QVBoxLayout()
        # 앞 버스정보 출력
        self.front_bus = self.busplay('000000000','서울00사0000')
        # 내 버스정보 출력
        self.target_bus = self.busplay('000000000','서울00사0000')
        # 뒤 버스정보 출력
        self.back_bus = self.busplay('000000000','서울00사0000')
        boxx.addWidget(self.front_bus)
        boxx.addWidget(self.target_bus)
        boxx.addWidget(self.back_bus)
        hbox.addLayout(boxx)
        gb2.setLayout(hbox)
        gb2.setStyleSheet("border-image: url(image/busbus.jpg);")
        busbox.addWidget(gb2)

        boxes = QHBoxLayout()
        boxes.addLayout(vbox)
        boxes.addLayout(busbox)
        self.setLayout(boxes)

        self.bus_time = QTimer(self)
        self.bus_time.setInterval(1000)
        self.bus_time.timeout.connect(self.ref_bus)
        self.bus_time.start()

        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.refresh)
        self.time.start()

    def ref_bus(self):

        if len(self.b.front) > 0:
            front_info = self.b.front
            front_id = str(list(front_info['plainNo'])[0])
            front_station = self.l.getstationNm(int(front_info['sectOrd'].values[0]))
            self.front_bus.setText(front_id+'\n\n'+front_station)
            self.front_st.setText(str(int(front_info['sectOrd'].values[0]) - int(self.b.target['sectOrd'].values[0])))
            
        if len(self.b.back) > 0:
            back_info = self.b.back
            back_id = str(list(back_info['plainNo'])[0])
            back_station = self.l.getstationNm(int(back_info['sectOrd'].values[0]))
            self.back_bus.setText(back_id+'\n\n'+back_station)
            self.front_st.setText(str(int(self.b.target['sectOrd'].values[0]) - int(back_info['sectOrd'].values[0])))
        if len(self.b.target) > 0:
            self.target_bus.setText(bus_No+'\n\n'+self.l.getstationNm(int(self.b.target['sectOrd'].values[0])))
        

    def refresh(self):
        try:
            self.fall_sig
        except:
            return
        # print(int(self.b.target['stopFlag']))
        # print(int(self.fall_sig))
        # print(int(self.l.Nmtostation(int(self.b.target['sectOrd'].values[0]))))
        if int(self.fall_sig) == int(self.l.Nmtostation(int(self.b.target['sectOrd'].values[0]))):
            self.s.receive_img(self.bus_id)
            stop_img = "image/fall_detected.jpg"
            self.lb_station.setText('사고: '+self.l.stationNm(int(self.fall_sig)))
            if int(self.b.target['stopFlag']):
                self.s.down_fall_sig(self.bus_id)
        elif int(self.stop_sig) == int(self.l.Nmtostation(int(self.b.target['sectOrd'].values[0]))): 
            stop_img = "image/stop.jpg"
            self.lb_station.setText('승차: '+self.l.stationNm(int(self.stop_sig)))
        else:
            stop_img = "image/main.jpg"
            self.lb_station.setText('사고: '+self.l.getstationNm(int(self.b.target['sectOrd'].values[0])))
        if int(self.stop_sig) == int(self.l.Nmtostation(int(self.b.target['sectOrd'].values[0]))):
            logo_img = "image/bus_stop.jpg"
        else:
            logo_img = "image/logo.jpg"

        self.img_label.setPixmap(QPixmap(QPixmap(stop_img)).scaledToHeight(image_width))
        self.lb_logo.setPixmap(QPixmap(QPixmap(logo_img)).scaledToHeight(140))

    def interval_receive(self):
        self.s.receive(self.bus_id)
        self.stop_sig = self.s.bus_info['stop_sig']
        self.fall_sig = self.s.bus_info['fall_sig']
        
        t = Timer(2, self.interval_receive)
        t.start()

    def bus_receive(self):
        self.b.targetinfo()
        t = Timer(2, self.bus_receive)
        t.start()

    def showtime(self):
        t = time.time()
        kor = time.localtime(t)
        label_time = '%02d:%02d:%02d' % (kor.tm_hour,kor.tm_min,kor.tm_sec)
        self.label.setText(label_time)
        self.label.setAlignment(Qt.AlignCenter)
        timer = Timer(1, self.showtime)
        timer.start()
    
    def busplay(self, station, name):
        lb = QLabel()
        lb.setText('     '+name+'\n\n'+station)
        lb.setStyleSheet("color: #004195;"
                        "font: 20pt;"
                        "font: bold;"
                        "border-image: url()")
        lb.setFixedSize(280,320)
        return lb

    def stations(self, stations=0):
        lbl = QLabel()
        lbl.setFixedSize(120,320)
        if stations:
            lbl.setText(str(stations))
        lbl.setStyleSheet("border-image: url();"
                          "color: #004195;"
                          "font: 36pt;"
                          "font: bold;")
        return lbl

 
if __name__ == '__main__':
    os.chdir('C:\\Users\\bbiuy\\Documents\\1_Workspace\\python\\bus_driver')
    app = QApplication(sys.argv)
    w = BusWidget()
    w.showFullScreen()
    sys.exit(app.exec_())