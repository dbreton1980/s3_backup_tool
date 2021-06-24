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

def backup_directory():
    """Check if backup directory exist, if don't exists, create it."""
    print(' \n Checking for backup directory ... %s ' %your_backup_directory)
    if (os.path.exists(your_backup_directory)) and (os.path.isdir(your_backup_directory)):
        print('  Backup directory found. ')
        time.sleep(1)
    else:
        print(' Backup directory not found ')
        print(' Creating backup directory ... %s ' %your_backup_directory)
        try:
            os.makedir(your_backup_directory)
            if not os.path.exists(your_backup_log):
                os.mknod(your_backup_log)
            f = open(your_backup_log, 'w')
            f.close()
            print(' Backup directory successfully created. ')
            time.sleep(1)
        except:
            print(' An error occurred while creating the directory ... ')
            print(' Try creating the directory %s manually and rerun the script ' %(your_backup_directory))
            sys.exit(0)
    f = open(your_backup_log,'a')
    f.write('%s: info: Backup started by user:%s \n'%(datetime.now().strftime("%d-%m-%Y à %H%M%S"),os.getlogin()))
    f.close()
    time.sleep(1)

def deleting_old_backups():
    max_backup = 5
    existing_backups = [
    x for x in your_backup_directory_path.iterdir()
    if x.is_file() and x.suffix == '.zip' and x.name.startswith('Sauvegarde')]
    oldest_to_newest_backup_by_name = list(sorted(existing_backups, key=lambda f: f.name))
    
    while len(oldest_to_newest_backup_by_name) >= max_backup:  
        backup_to_delete = oldest_to_newest_backup_by_name.pop(0)
        backup_to_delete.unlink()
        print('  Deleting old backups... ')
        time.sleep(1)
        
def backup_to_zip():
    """Zip your source directory."""
    print('  The following files and directories will be backuped up. ')
    backup_file_name = f'Sauvegarde du dossier {your_source_directory_path.name} du {datetime.now().strftime("%d-%m-%Y à %H%M%S")}.zip'
    zip_file = zipfile.ZipFile(str(your_backup_directory_path / backup_file_name), mode='w', )
    if your_source_directory_path.is_file():
    # File backup
        zip_file.write(
        your_source_directory_path(),
        arcname=your_source_directory_path.name,
        compress_type=zipfile.ZIP_DEFLATED
    )
    elif your_source_directory_path.is_dir():
    # Directory backup
        for file in your_source_directory_path.glob('**/*'):
            if file.is_file():
                zip_file.write(
                file.absolute(),
                arcname=str(file.relative_to(your_source_directory_path)),
                compress_type=zipfile.ZIP_DEFLATED
                )
    # Zip processus end
        zip_file.close()
    print(' \n  Backup completed successfully \n  Backup stored in %s ' %(your_backup_directory))
    

def upload_to_aws():
    """Upload of zip's folder zipped."""
    connexion = boto.connect_s3(your_aws_access_key_id,
                            your_aws_access_key_secret,
                            host=your_region_host)
    nonexistent = connexion.lookup(your_amazon_bucket)
    # Check if the bucket exists and initialize connection, if doesn't exists, bucket is create.
    if nonexistent is None:
        print ('Bucket doesn t exist. Creating bucket...')
        bucket = connexion.create_bucket(your_amazon_bucket, location="eu-west-3")
    else:
        bucket = connexion.get_bucket(your_amazon_bucket, validate=True)
    # Start of uploading on S3 bucket.
    try:
        upload_file_names = []
        for root, dirs, files in os.walk(your_backup_directory, topdown=False):
            for name in files:
                fname=os.path.join(root, name)
                upload_file_names.append(fname)
                print (upload_file_names)

            for filenames in upload_file_names:
                filename=filenames.replace("\\", "/")
                sourcepath = filename
                destpath = filename

            k = boto.s3.key.Key(bucket)
            k.key = destpath
#            k.set_contents_from_filename(sourcepath,cb=percent_cb, num_cb=10)
            print("Upload Successful")
            return True

    except FileNotFoundError:
        print("The file was not found")
        return False

def mailer():
    """This function sends an email to user with log file."""
    print('  Sending Mail ... ')
    f = open(your_backup_log)
    for line in f.readlines():
        pass
    print(line)
    print('  An email has been sent to you... ')
    msg = MIMEMultipart()
    msg['From'] = your_email_address
    msg['To'] = your_email_address
    msg['Subject'] = ' S3_Backup LOG Notification '
    nom_fichier = "backup.log"
    piece = open(your_backup_log, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((piece).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "piece; filename= %s" % nom_fichier)
    msg.attach(part)
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(your_email_address, your_psw)
    mailserver.sendmail(your_email_address, your_email_address, msg.as_string())
    mailserver.quit()
    