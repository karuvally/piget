#!/usr/bin/env python3
# piget (Alpha release)
# Copyright 2017, Aswin Babu Karuvally

# import some serious stuff
from ftplib import FTP
from paramiko import client
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


# create checksum for the remote files
def create_remote_checksum(server, ssh_user, ssh_pass, file):
    # declare some essential variables
    remote_checksum = ""
    
    # initiate the connection
    ssh_connection = client.SSHClient()
    ssh_connection.set_missing_host_key_policy(client.AutoAddPolicy())
    ssh_connection.connect(server, username=ssh_user, password=ssh_pass)
    
    # execute the command, receive output
    stdin, stdout, stderr = ssh_connection.exec_command(file)
    while not stdout.channel.exit_status_ready():
        while stdout.channel.recv_ready():
            remote_checksum += str(stdout.channel.recv(1024), 'utf8')
    
    # close connection and return checksum
    ssh_connection.close()
    return remote_checksum


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
            retrieve_files(ftp_connection, configuration, file)
        else:
            ftp_connection.retrbinary('RETR ' + file, open(file, 'wb').write)
    
    # move one level up the file system
    ftp_connection.cwd('..') # debug
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
    ftp_connection.quit()


# call the main function
main()
