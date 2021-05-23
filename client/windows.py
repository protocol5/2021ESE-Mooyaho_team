# -*- coding: cp949 -*- 

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import client
 
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

ipaddress = "192.168.0.2"
port = 5614
 
class CWidget(QWidget):
    def __init__(self):
        super().__init__()  
         
        self.c = client.ClientSocket(self)
        
        self.initUI()
 
    def __del__(self):
        self.c.stop()
 
    def initUI(self):
        self.setWindowTitle('클라이언트')
         
        ipbox = QHBoxLayout()
 
        gb = QGroupBox('서버 설정')
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
 
        self.btn = QPushButton('접속')       
        self.btn.clicked.connect(self.connectClicked)
        box.addWidget(self.btn)
 
        gb.setLayout(box)

        infobox = QHBoxLayout()      
        gb = QGroupBox('메시지')        
        infobox.addWidget(gb)
 
        box = QVBoxLayout()

        label = QLabel('받은 메시지')
        box.addWidget(label)
 
        self.recvmsg = QListWidget()
        self.recvmsg.setFixedHeight(100)
        box.addWidget(self.recvmsg)
 
        label = QLabel('보낸 메시지')
        box.addWidget(label)
        
        self.sendmsg = QTextEdit()
        self.sendmsg.setFixedHeight(30)
        box.addWidget(self.sendmsg)
 
        hbox = QHBoxLayout()
 
        box.addLayout(hbox)
        self.sendbtn = QPushButton('보내기')
        self.sendbtn.setAutoDefault(True)
        self.sendbtn.clicked.connect(self.sendMsg)
 
        hbox.addWidget(self.sendbtn)
        gb.setLayout(box)
 
        vbox = QVBoxLayout()
        vbox.addLayout(ipbox)       
        vbox.addLayout(infobox)
        self.setLayout(vbox)
         
        self.show()
 
    def connectClicked(self):
        if self.c.bConnect == False:
            ip = self.ip.text()
            port = self.port.text()
            if self.c.connectServer(ip, int(port)):
                self.btn.setText('접속종료')
            else:
                self.c.stop()
                self.sendmsg.clear()
                self.recvmsg.clear()
                self.btn.setText('접속')
        else:
            self.c.stop()
            self.sendmsg.clear()
            self.recvmsg.clear()
            self.btn.setText('접속')
 
    def updateMsg(self, msg):
        self.recvmsg.addItem(QListWidgetItem(msg))
    
    def updatePic(self, path):
        self.dialog = QDialog()
        self.dialog.setWindowTitle('Fall Detection Image')
        self.dialog.setWindowModality(Qt.ApplicationModal)
        
        label = QLabel()
        label.setPixmap(QPixmap(path))

        pbox = QVBoxLayout()
        pbox.addWidget(label)
        self.dialog.setLayout(pbox)

        self.dialog.show()
        
 
    def updateDisconnect(self):
        self.btn.setText('접속')
 
    def sendMsg(self):
        sendmsg = self.sendmsg.toPlainText()
        self.c.send(sendmsg)
        self.sendmsg.clear()
 
    def clearMsg(self):
        self.recvmsg.clear()
 
    def closeEvent(self, e):
        self.c.stop()       
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CWidget()
    sys.exit(app.exec_())