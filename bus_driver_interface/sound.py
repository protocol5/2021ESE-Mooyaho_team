# -*- coding: cp949 -*- 

import os
import sys
from PyQt5 import QtCore
import QtMultimedia 5.15
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
def main():
    filename = os.path.join(CURRENT_DIR, "mooyaho.mp3")
    app = QtCore.QCoreApplication(sys.argv)
    player = QtMultimedia.QMediaPlayer()
    url = QtCore.QUrl.fromLocalFile(filename)
    player.setMedia(QtMultimedia.QMediaContent(url))
    player.play()
    # end in 5 seconds:
    QtCore.QTimer.singleShot(5 * 1000, app.quit)
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()