import cv2
import os
import time

# image file path
img_file = '/home/pi/ftp/files/fall_detected.jpg'

# get modified time of image first
modTimesinceEpoc = os.path.getmtime(img_file)
modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
print("Last Modified Time : ", modificationTime)

count = 0
# keep loop for showing image (when modified time is changed)
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

    # if count = 1, wait 3 seconds for rewriting the image and imshow for 2 seconds
    if count == 1:
        time.sleep(1)
        image = cv2.imread(img_file, cv2.IMREAD_COLOR)
        cv2.imshow('wow', image)
        cv2.waitKey(2000)
    # else, close the image and continue
    else:
        cv2.destroyAllWindows()
        continue

    # renewal the variable (modified time)
    modificationTime = modificationTime_recent

cv2.destroyAllWindows()