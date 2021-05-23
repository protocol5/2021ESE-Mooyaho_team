# -*- coding: cp949 -*-

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import socket
import server
 
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

ipaddress = "192.168.0.2"
port = 5614
 
class CWidget(QWidget):
    def __init__(self):
        super().__init__()
 
        self.s = server.ServerSocket(self)
        
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle('����')
        
        ipbox = QHBoxLayout()
 
        gb = QGroupBox('���� ����')
        ipbox.addWidget(gb)
 
        box = QHBoxLayout()
 
        label = QLabel('Server IP')
        self.ip = QLineEdit(ipaddress)
        box.addWidget(label)
        box.addWidget(self.ip)
 
        label = QLabel('Server Port')
        self.port = QLineEdit(str(port))
        box.addWidget(label)
        box.addWidget(self.port)
 
        self.btn = QPushButton('���� ����')
        self.btn.setCheckable(True)        
        self.btn.toggled.connect(self.toggleButton)
        box.addWidget(self.btn)     
 
        gb.setLayout(box)
 
        infobox = QHBoxLayout()
        gb = QGroupBox('���� ����')
        infobox.addWidget(gb)
 
        box = QHBoxLayout()        
 
        self.guest = QTableWidget()        
        self.guest.setColumnCount(1)
        self.guest.setHorizontalHeaderItem(0, QTableWidgetItem('���� ��ȣ'))         
 
        box.addWidget(self.guest)
        gb.setLayout(box)
 
        box = QVBoxLayout()        
 
        gb.setLayout(box)
 
        vbox = QVBoxLayout()
        vbox.addLayout(ipbox)       
        vbox.addLayout(infobox)
        self.setLayout(vbox)
         
        self.show()
 
    def toggleButton(self, state):
        if state:
            ip = self.ip.text()
            port = self.port.text()
            if self.s.start(ip, int(port)):
                self.btn.setText('���� ����')                
        else:
            self.s.stop()
            self.msg.clear()
            self.btn.setText('���� ����')
 
    def updateClient(self, addr, isConnect = False):        
        row = self.guest.rowCount()
        if isConnect:        
            self.guest.setRowCount(row+1)
            self.guest.setItem(row, 0, QTableWidgetItem(str(addr[1])))
        else:            
            for r in range(row):
                ip = self.guest.item(r, 0).text() # ip
                port = self.guest.item(r, 1).text() # port
                if addr[0]==ip and str(addr[1])==port:
                    self.guest.removeRow(r)
                    break
 
    def closeEvent(self, e):
        self.s.stop()
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())