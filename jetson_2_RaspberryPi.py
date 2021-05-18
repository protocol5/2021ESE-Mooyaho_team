import cv2
import ftplib
import os
import time

# image file path
img_file = '/home/myh/2021ESE-Mooyaho_team/darknet/fall_detected.jpg'

# get modified time of image first
modTimesinceEpoc = os.path.getmtime(img_file)
modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
print("Last Modified Time : ", modificationTime)


# keep loop for showing image (when modified time is changed)
count = 0
while(1):
    # get modified time again to compare
    modTimesinceEpoc_recent = os.path.getmtime(img_file)
    modificationTime_recent = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc_recent))
    print("Last Modified Time : ", modificationTime_recent)

    # if modified time is different with before time, count = 1
    if modificationTime_recent != modificationTime:
        count = 1
    # else, count = 0
    else:
        count = 0

    # if count = 1, wait 1 second for rewriting the image and imshow for 2 seconds
    if count == 1:
        time.sleep(1)
        filename = 'fall_detected.jpg'
        ftp = ftplib.FTP("192.168.1.7")
        ftp.login("pi", "gkseogns12")
        ftp.cwd("files")
        os.chdir(r"/home/myh/2021ESE-Mooyaho_team/darknet/")
        with open(filename, 'rb') as contents:
            ftp.storbinary("STOR {}".format(os.path.basename(filename)), contents)
            contents.close()
        ftp.quit()
    # else, close the image and continue
    else:
        continue

    # renewal the variable (modified time)
    modificationTime = modificationTime_recent
