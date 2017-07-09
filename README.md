# Piget 
Automated File Retrieval tool 

## Introduction 
Piget is an FTP based automated file retrieval tool. 
It retrieves entire remote directories periodically,
then deletes the original files.

## Why?
My home surveillance system is a Raspberry Pi having limited memory. 
This is very handy, as it will automatically move the remote directory, 
containing surveillance footage to my workstation.

## Why not just use wget and cron? 
Piget will eventually allow me to do checksum for each file, making sure it is not
faulty before deleting the originals. Also, creating this was a fun experience

## Installation
- Clone the repository or download it as zip
- Unzip the contents to a convenient directory
- Make piget.py executable by running chmod +x piget.py
- Copy piget.conf to /home/<user_name>/.config/piget.conf
- Edit the configuration as per your configuration, leave the ssh stuff
- As root, run ln -s /path/to/piget.py /usr/bin/piget
- Run piget using the command "piget" from your terminal
- Add the executable to cron if you want piget to run periodically

## To-Do
- Integrity check for transferred files
- Better exception handling (which is non-existant at the moment)
