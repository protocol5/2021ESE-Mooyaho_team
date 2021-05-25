import cv2
import ftplib
import os
import time
import paramiko

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

        # connect GCP with ssh
        host = '34.64.138.186'
        username = 'moyahoo'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # need to modify keyfilename@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        ssh.connect(host, username=username, key_filename='/home/myh/Desktop/myh_keyfile.pem')
        #########################################################

        # sftp open
        sftp = ssh.open_sftp()
        print("connect success")

        # file upload
        filename = 'fall_detected.jpg'
        os.chdir(r"/home/myh/2021ESE-Mooyaho_team/darknet/")
        with open(filename, 'rb') as contents:
            sftp.chdir('/home/moyahoo/fall_detection')
            sftp.put('/home/myh/2021ESE-Mooyaho_team/darknet/fall_detected.jpg', 'fall_detected.jpg')
            contents.close()
        

        sftp.close()
        ssh.close()
        

    # else, close the image and continue
    else:
        continue

    # renewal the variable (modified time)
    modificationTime = modificationTime_recent
