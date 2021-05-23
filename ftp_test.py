import cv2
import ftplib
import os
import time

# image file path
img_file = '/home/myh/2021ESE-Mooyaho_team/darknet/fall_detected.jpg'

filename = 'fall_detected.jpg'
#ftp = ftplib.FTP("192.168.1.7")
ftp = ftplib.FTP("172.16.63.157")
ftp.login("pi", "gkseogns12")
ftp.cwd("files")
os.chdir(r"/home/myh/2021ESE-Mooyaho_team/darknet/")
with open(filename, 'rb') as contents:
    ftp.storbinary("STOR {}".format(os.path.basename(filename)), contents)
    contents.close()
ftp.quit()


