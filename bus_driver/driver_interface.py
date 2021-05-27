# -*- coding: cp949 -*- 

from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from threading import Timer
import time
import sys, os
import pymysql
import pandas as pd
import server

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

image_width = 800

class BusWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.s = server.SQL()

        self.label = QLabel()
        font = QFont('Arial', 30)
        self.label.setFont(font)
        self.label.setStyleSheet("border-image: url()")

        # background image 무야호
        bgimg = QImage('image\\background.jpg')
        palette = QPalette()
        palette.setBrush(10, QBrush(bgimg))
        self.setPalette(palette)

        # server 연결
        self.s.connect()
        self.interval_receive()

        self.initUI()
 
    def initUI(self):
        
        self.setWindowTitle('Bus Driver Display')
        # self.resize(500,500)

        # text box
        lbox = QHBoxLayout()
        box = QHBoxLayout()
        self.lb_logo = QLabel(self)
        self.lb_logo.setPixmap(QPixmap(QPixmap('image//logo.jpg')).scaledToWidth(300))
        self.lb_logo.setFixedSize(300,100)
        box.addWidget(self.lb_logo)
        self.lb_station = QLabel('현재: 청량리 환승 센터')
        self.lb_station.setStyleSheet("color: black;"
                         "font: 16pt;"
                         "font: bold;"
                         "border-style: solid;"
                         "border-width: 5px;"
                         "border-color: #7FFFD4")
        self.lb_station.setFixedSize(image_width-300,60)
        box.addWidget(self.lb_station)
        lbox.addLayout(box)

        # image box
        imgbox = QHBoxLayout()
        gb = QGroupBox('Bus Stop Image')
        imgbox.addWidget(gb)
        box = QHBoxLayout()
        self.img_label = QLabel(self)
        # label.setFixedSize(720,500)
        stop_img = "image/background.jpg"
        self.img_label.setPixmap(QPixmap(QPixmap(stop_img)).scaledToWidth(image_width))
        box.addWidget(self.img_label, alignment=Qt.AlignCenter)
        gb.setLayout(box)
        gb.setFixedWidth(image_width)
        vbox = QVBoxLayout()
        vbox.addLayout(lbox)
        vbox.addLayout(imgbox)

        # time box
        busbox = QVBoxLayout()
        gb = QGroupBox('')
        hbox = QHBoxLayout()
        hbox.addWidget(self.label)
        gb.setLayout(hbox)
        gb.setFixedSize(230,80)
        gb.setStyleSheet("border-image: url(image/clock.jpg)")
        busbox.addWidget(gb)

        self.showtime()

        # 앞앞 버스정보 출력
        busbox.addWidget(self.busplay(7,'서울시립대 정문', '1001'))
        # 앞 버스정보 출력
        busbox.addWidget(self.busplay(3,'서울시립대 후문', '1002'))
        # 뒤 버스정보 출력
        busbox.addWidget(self.busplay(3,'서울시립대 쪽문', '1003'))
        # 뒤뒤 버스정보 출력
        busbox.addWidget(self.busplay(7,'서울시립대 9와 3/4', '1004'))

        boxes = QHBoxLayout()
        boxes.addLayout(vbox)
        boxes.addLayout(busbox)
        self.setLayout(boxes)

        self.time = QTimer(self)
        self.time.setInterval(2000)
        self.time.timeout.connect(self.refresh)
        self.time.start()

    def refresh(self):
        if int(self.fall_sig):
            stop_img = "image/fall.jpg"
            logo_img = "image/logo.jpg"
        elif int(self.stop_sig):
            stop_img = "image/stop.jpg"
            logo_img = "image/bus_stop.jpg"
        else:
            stop_img = "image/myh.jpg"
            logo_img = "image/logo.jpg"
        self.img_label.setPixmap(QPixmap(QPixmap(stop_img)).scaledToWidth(image_width))
        self.lb_logo.setPixmap(QPixmap(QPixmap(logo_img)).scaledToWidth(300))

    def interval_receive(self):
        self.s.receive(100100132)
        self.stop_sig = self.s.bus_info['stop_sig']
        self.fall_sig = self.s.bus_info['fall_sig']
        # print("server refresh\n", self.s.bus_info)
        t = Timer(10, self.interval_receive)
        t.start()

    def showtime(self):
        t = time.time()
        kor = time.localtime(t)
        label_time = '%02d:%02d:%02d' % (kor.tm_hour,kor.tm_min,kor.tm_sec)
        self.label.setText(label_time)
        timer = Timer(1, self.showtime)
        timer.start()
    
    def busplay(self, min, station, name):
        gb = QGroupBox()
        gb.setStyleSheet("border-image: url(image/bus.jpg)")
        box = QVBoxLayout()
        lb = QLabel(name+'번 '+ str(min) +'분')
        lb.setStyleSheet("color: white;"
                         "font: 12pt;"
                         "font: bold;"
                         "border-image: url()"
                         )
        lb.setFixedSize(200,30)
        lb.setAlignment(QtCore.Qt.AlignCenter)
        box.addWidget(lb)
        lb = QLabel(station)
        lb.setStyleSheet("color: white;"
                         "font: 12pt;"
                         "font: bold;"
                         "border-image: url()"
                         )
        lb.setFixedSize(200,40)
        lb.setAlignment(QtCore.Qt.AlignCenter)
        box.addWidget(lb)
        gb.setLayout(box)
        gb.setFixedSize(220,120)
        
        return gb

 
if __name__ == '__main__':
    os.chdir('C:\\Users\\bbiuy\\Documents\\1_Workspace\\python\\bus_driver')
    app = QApplication(sys.argv)
    w = BusWidget()
    w.show()
    sys.exit(app.exec_())