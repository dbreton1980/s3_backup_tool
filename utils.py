"""System module."""
import zipfile
import os.path
import sys
import time
import boto
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

def menu():
    """This function creates a menu to user."""
    print('=' * 50)
    print(' S3 Backup Tool Script ')
    print(' Dominique BRETON ')
    print('=' * 50)
    print(' 1. Backup your folder')
    print(' 2. Press any other key to exit  ')
    choice = input(' \n Enter Selection:  ')

    #Read the choice and process, stores input user in global variable.
    if choice == '1':
        time.sleep(1)
        print(' Beginning the backup process ... ')
        global your_source_directory
        your_source_directory = input("Enter your source directory path:")
        print('You said: %s' % your_source_directory)
        global your_backup_directory
        your_backup_directory = input("Enter your backup directory path:")
        print('You said: %s' % your_backup_directory)
        global your_backup_log
        your_backup_log = input("Enter your backup log path: ")
        print('You said: %s' % your_backup_log)
        global your_email_address
        your_email_address = input("Enter your email address: ")
        print('You said: %s' % your_email_address)
        global your_psw
        your_psw = input("Enter your password: ")
        print('You said: %s' % your_psw)
        global your_amazon_bucket
        your_amazon_bucket = input("Enter your amazon bucket name:")
        print('You said: %s' % your_amazon_bucket)
        global your_aws_access_key_id
        your_aws_access_key_id = input("Enter your AWS_ACCESS_KEY_ID:")
        global your_aws_access_key_secret
        your_aws_access_key_secret = input("Enter your AWS_ACCESS_KEY_SECRET:")
        global your_region_host
        your_region_host = input("Enter your REGION_HOST:")
        print('You said: %s' % your_region_host)
        os.environ['S3_USE_SIGV4'] = 'True'
        global your_source_directory_path
        your_source_directory_path = Path(your_source_directory)
        global your_backup_directory_path
        your_backup_directory_path = Path(your_backup_directory)
        while True:
            yes_no = input("Do you want to continue? Enter yes/no: ")
            yesChoice = ['yes', 'y', 'ye', 'Y']
            noChoice = ['no', 'n', 'N']
            if yes_no in yesChoice:
                break
            if yes_no in noChoice:
                menu()
                
    elif choice == '2':
        print(' \n Exiting ... ')
        sys.exit(1)
    elif choice == '2':
        print(' \n Exiting ... ')
        sys.exit(1)
    else:
        print(' Invalid choice. ')
        time.sleep(1)
        menu()

def source_directory():
    """Check if source directory exist, if don't exists, create it."""
    print('  \n Checking for source directory ... %s  ' %your_source_directory)
    time.sleep(1)
    try:
        os.makedirs(your_source_directory)
        print("  Directory " , your_source_directory ,  " created. ")
    except FileExistsError:
        print("  Directory " , your_source_directory ,  " already exists. ")
