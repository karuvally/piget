#!/usr/bin/env python3
# piget (Alpha release)
# Copyright 2017, Aswin Babu Karuvally

# import some serious stuff
from ftplib import FTP


# retrieve files from the server
def retrieve_files(directory_path):
	pass


# the main function
def main():
	# set up the connection
	ftp_connection = FTP('karuvally.org')
	ftp_connection.login(user='pi', passwd='karuvally')
	
	# change to desired directory and list contents
	ftp_connection.cwd('/home/pi')
	file_list = ftp_connection.nlst()
	
	#print(file_list) #debug
	
	ftp_connection.retrbinary('RETR bak.zip', open('bak.zip', 'wb').write)
	
	# log off from the connected machine
	ftp_connection.quit()


# call the main function
main()
