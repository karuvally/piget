#!/usr/bin/env python3
# piget (Alpha release)
# Copyright 2017, Aswin Babu Karuvally

# import some serious stuff
from ftplib import FTP


# the function where stuff happens
def retrieve_files(ftp_connection, directory_path):
	# set up some essential variables
	file_type_list = []
	file_dictionary = {}
	
	# get the file information
	ftp_connection.cwd(directory_path)
	ftp_connection.retrlines('LIST', file_type_list.append)
	file_list = ftp_connection.nlst()
	
	# create a dictionary containing file information
	for i in range(0, len(file_list)):
		file_dictionary[file_list[i]] = file_type_list[i][0]
	
	# retrieve the files
	for file in file_dictionary:
		if(file_dictionary[file]) == 'd':
			os.mkdir(file)
			os.chdir(file)
			retrieve_files(ftp_connection, file)
		else:
			ftp_connection.retrbinary('RETR' + file, open(file, 'wb').write)
	
	# move one level up the file system
	ftp_connection.cwd('..') # debug
	os.chdir('..')


# the main function
def main():
	# essential stuff
	server = 'karuvally.org'
	directory_path = '/home/pi/downloads/'
	username = 'pi'
	password = 'karuvally'
	
	# set up the connection
	ftp_connection = FTP(server)
	ftp_connection.login(user=username, passwd=password)
	
	# retrieve files and quit
	retrieve_files(ftp_connection, directory_path)
	ftp_connection.quit()


# call the main function
main()
