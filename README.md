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
