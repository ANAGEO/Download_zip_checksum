#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 10:42:15 2020

@author: tais
"""

# Import libraries
import os
import urllib.request
import shutil
import hashlib
from zipfile import ZipFile 
from os.path import basename

# Define functions
def CheckSUM(path_file, path_md5):   
    '''
    Function to check if the file downloaded correspond to the md5sum file provided. 
    The trick comes from here: https://stackoverflow.com/questions/16874598/how-do-i-calculate-the-md5-checksum-of-a-file-in-python
    '''
    try:
        # Get original md5 
        original_md5 = open(path_md5,'r').read().split(" ")[0]
        # Open,close, read file and calculate MD5 on its contents 
        with open(path_file, 'rb') as file_to_check:
            # read contents of the file
            data = file_to_check.read()    
            # pipe contents of the file through
            md5_returned = hashlib.md5(data).hexdigest()
        # Finally compare original MD5 with freshly calculated
        if original_md5 == md5_returned:
            return True
        else:
            return False
    except:
        return False

def DownloadFile(url,destination_folder):
    '''
    Function to download file from URL. The file will be saved in the destination folder with the same name as in the URL.
    '''
    try:
        name = url.split('/')[-1]
        path_newfile = os.path.join(destination_folder,name)
        with urllib.request.urlopen(url) as response, open(path_newfile, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        return True, path_newfile
    except:
        return False, False

def ZipFiles(list_of_files):
    '''
    Function to create a zip folder with files.
    '''
    try:
        import zipfile
        try:
            import zlib
            compression = zipfile.ZIP_DEFLATED
        except:
            compression = zipfile.ZIP_STORED
        zipped = '%s.zip'%os.path.splitext(list_of_files[0])[0]
        with ZipFile(zipped,'w') as zip: 
            # writing each file one by one 
            for file in list_of_files: 
                zip.write(file,basename(file),compress_type=compression)
                os.remove(file)
        return True
    except:
        return False
    

def DownloadCheckAndZipFile(url):
    '''
    Function to download file from URL and check the md5sum file.
    '''
    try:
        succeed_download = True
        succeed_check = True
        succeed_zip = True
        list_files_for_ip = []
        name = url.split('/')[-1]
        succeed_download, dowloaded_file = DownloadFile(url,destination_folder)
        list_files_for_ip.append(dowloaded_file)
        if not succeed_download:
            print("ERROR: An error occured with download of file '%s'."%name)
        else:
            if name.split('.')[-1] not in ('pdf'):  # Verify md5sum for each files type except .pdf
                url_md5 = '%s.md5sum'%url
                succeed_download, md5file = DownloadFile(url_md5,destination_folder)
                list_files_for_ip.append(md5file)
                if not succeed_download:
                    print("ERROR: An error occured with download of .md5sum file '%s.md5sum'."%name)
                else:
                    succeed_check = CheckSUM(dowloaded_file,md5file)
                    if not succeed_check:
                        print("ERROR: Verification of .md5sum failed for file '%s'."%name)
                    else:
                        succeed_zip = ZipFiles(list_files_for_ip)
                        if not succeed_zip:
                            print("ERROR: An error occured when zipping files '%s'."%','.join(list_files_for_ip))
                        else:
                            print("File '%s' successfully downloaded."%name)
    except:
         print("FATAL ERROR: An error occured during the execution of the script.")


##### MAIN #####
cities = []
#cities.append("Luanda_AO_20170825")
cities.append("Accra_GH_20190211")
cities.append("Lagos_NI_20190606")
cities.append("Abidjan_IV_20190802")
cities.append("Dhaka_BG_20190816")
cities.append("Kinshasa_CF_20191019")
cities.append("Ibadan_NI_20200122")
cities.append("Dakar_SG_20200309")
cities.append("Kano_NI_20200312")
cities.append("Addis_Ababa_ET_20200415")
cities.append("Nairobi_KE_20190515")
cities.append("Ouagadougou_UV_20200110")

for a in cities:
    # User parameters
    list_file = "/media/tais/My_Book_1/Images_COVID/%s/download_links.txt"%a
    destination_folder = os.path.split(list_file)[0]
    
    # Get list of URL
    with open(list_file,'r') as fin:
        list_urls = [a.strip() for a in fin.readlines()]
        list_urls_files = [a.strip() for a in list_urls if os.path.splitext(a)[-1]!='.md5sum'] # Keep only url of files which are not .md5sum
    
    # Download files 
    for url in list_urls_files:
        DownloadCheckAndZipFile(url)