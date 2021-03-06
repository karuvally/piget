#!/usr/bin/env python3
# piget (Alpha release)
# Copyright 2017, Aswin Babu Karuvally

# import some serious stuff
from ftplib import FTP
import os


# read and process configuration
def read_configuration_file(configuration_file_path):
    # essential variables
    configuration_dictionary = {}
    
    # read file and generate dictionary
    configuration_file = open(configuration_file_path, 'r')
    for line in configuration_file:
        if line[0] == '#' or not line.strip():
            continue
        else:
            configuration = line.strip().split('=')
            configuration_dictionary[configuration[0]] = configuration[1]
    
    # close file and return data
    configuration_file.close()
    return configuration_dictionary


# the function where stuff happens
def retrieve_files(ftp_connection, configuration, current_file_path):
    # set up some essential variables
    file_type_list = []
    file_dictionary = {}
    
    # get the file information
    ftp_connection.cwd(current_file_path)
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
            current_file_path += '/' + file
            retrieve_files(ftp_connection, configuration, current_file_path)
        else:
            # do the checksum thing here
            ftp_connection.retrbinary('RETR ' + file, open(file, 'wb').write) #debug
            
        #delete original files
        if configuration['delete_files'] == 'enabled':
            try:
                ftp_connection.delete(file)
            except Exception:
                ftp_connection.rmd(file)
    
    # move one level up the file system
    ftp_connection.cwd('..')
    os.chdir('..')


# the main function
def main():
    # read the confugration file
    configuration_file_path = '/home/' + os.getlogin() + '/.config/piget.conf'
    configuration = read_configuration_file(configuration_file_path)
    
    # set up the ftp connection
    ftp_connection = FTP(configuration['ftp_server'])
    ftp_connection.login(user=configuration['ftp_username'], passwd=configuration['ftp_password'])
    
    # retrieve files and quit
    retrieve_files(ftp_connection, configuration, configuration['remote_file_path'])
    
    # close the ftp connection
    ftp_connection.quit()


# call the main function
main()
