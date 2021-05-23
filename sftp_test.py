import paramiko

# bus stop id
bus_stop_id = '105000102'

# connect GCP with ssh
host = '34.64.183.238'
username = 'moyahoo'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, username=username, key_filename='/home/myh/Desktop/myh_keyfile.pem')


# sftp open
sftp = ssh.open_sftp()
print("connect success")


# file download
#sftp.chdir('/home/moyahoo/fall_detection')
#print(sftp.getcwd())
#sftp.get('cap.JPG', '/home/myh/Desktop/cap.jpg')


# file upload
sftp.chdir('/home/moyahoo/fall_detection')
sftp.put('/home/myh/Pictures/darknet.png', 'darknet.jpg')


# cd to fall_detection and print ls
#stdin, stdout, stderr = ssh.exec_command('cd fall_detection;ls')
#print(stdout.readlines())

sftp.close()
ssh.close()
