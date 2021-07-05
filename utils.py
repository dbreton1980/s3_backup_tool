import boto
import boto3
import os
import pyzipper
import smtplib
import sys
import time


from getpass import getpass
from pathlib import Path
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def get_all_choices():
    """
    Allows to collect all the parameters necessary for the operation of the backup
    
    Returns
    -------
    choices: dict
        All choices to execute full process.
    """
    choices = {}
    choices['your_source_directory'] = input(" Enter your source directory path: ")
    choices['your_backup_directory'] = input(" Enter your backup directory path: ")
    choices['your_password'] = getpass(prompt=" Enter your password to protect your archive: ")
    choices['your_backup_log'] = input(" Enter your backup log path: ")
    choices['your_email_address'] = input(" Enter your email address: ")
    choices['your_psw'] = getpass(prompt=" Enter your email password: ")
    choices['your_amazon_bucket'] = input(" Enter your amazon bucket name: ")
    choices['your_aws_access_key_id'] = input(" Enter your AWS_ACCESS_KEY_ID: ")
    choices['your_aws_access_key_secret'] = input(" Enter your AWS_ACCESS_KEY_SECRET: ")
    choices['your_region_host'] = input(" Enter your REGION_HOST: ")

    return choices


def get_menu_choice():
    """
    Display the menu and display a choice
    """
    print('=' * 60)
    print(' S3 Backup Tool Script ')
    print(' Dominique BRETON ')
    print('=' * 60)
    print(' 1. Create your source directory ')
    print(' 2. Create your backup directory ')
    print(' 3. Display your Amazon S3 bucket list ')
    print(' 4. Create your Amazon S3 bucket ')
    print(' 5. Remove your Amazon S3 bucket ')
    print(' 6. Full backup ')
    print(' 7. Upload on Amazon S3 ')
    print(' h. Help menu ')
    print(' q. Quit ')
    return input(' \n Enter Selection:  ')

def source_directory(your_source_directory):
    """
    Check if source directory exist, if don't exists, create it.

    Parameters
    ----------
    your_source_directory: str
        Path of source directory
    """
    print('=' * 60)
    print(' \n Checking for source directory ... %s  ' %your_source_directory)
    time.sleep(1)
    try:
        os.mkdir(your_source_directory)
        print(" Directory ", your_source_directory ," created. \n")
    except FileExistsError:
        print(" Directory ", your_source_directory ," already exists. \n")
    print('=' * 60)

def backup_directory(your_backup_directory):
    """
    Check if backup directory exist, if don't exist, create it.

    Parameters
    ----------
    your_backup_directory: str
        Path of backup directory
    """
    print('=' * 60)
    print(' \n Checking for backup directory ... %s ' %your_backup_directory)
    if (os.path.exists(your_backup_directory)) and (os.path.isdir(your_backup_directory)):
        print(" Directory" , your_backup_directory ,  "already exists. \n " )
        time.sleep(1)
    else:
        print(' Backup directory not found ')
        print(' Creating backup directory ... %s ' %your_backup_directory)
        try:
            os.mkdir(your_backup_directory)
            print(' Backup directory successfully created. \n')
            time.sleep(1)
        except:
            print(' An error occurred while creating the directory ... ')
            print(' Try creating the directory %s manually and rerun the script ' %(your_backup_directory))
            sys.exit(0)
    print('=' * 60)

def list_bucket(your_aws_access_key_id, your_aws_access_key_secret, your_region_host):
    """
    List all buckets for a given aws account.

    Parameters
    ----------
    your_aws_access_key_id: str
        AWS acces key id.

    your_aws_access_key_secret: str
        AWS key secret.

    your_region_host: str
        Region a given AWS account.
    """
    os.environ['S3_USE_SIGV4'] = 'True'
    connexion = boto.connect_s3(
        your_aws_access_key_id,
        your_aws_access_key_secret,
        host=your_region_host
    )
    
    buckets = connexion.get_all_buckets()
    print('=' * 60)
    for key in buckets:
        print(f'Bucket Name: {key.name}')
    print('=' * 60)
    time.sleep(1)


def create_bucket(your_amazon_bucket, your_aws_access_key_id, your_aws_access_key_secret, your_region_host):
    """
    Create buckets for a given aws account.

    Parameters
    ----------
    your_amazon_bucket: str
        AWS bucket name.

    your_aws_access_key_id: str
        AWS acces key id.

    your_aws_access_key_secret: str
        AWS key secret.

    your_region_host: str
        Region a given AWS account.
    """
    os.environ['S3_USE_SIGV4'] = 'True'
    connexion = boto.connect_s3(
        your_aws_access_key_id,
        your_aws_access_key_secret,
        host=your_region_host
    )
    nonexistent = connexion.lookup(your_amazon_bucket)
    # Check if the bucket exists and initialize connection, if doesn't exists, bucket is create.
    if nonexistent is None:
        bucket = connexion.create_bucket(your_amazon_bucket, location="eu-west-3")
        print('=' * 60)
        print(' Bucket doesn''t exist.')
        print(' Creating bucket %s ...' %your_amazon_bucket)
        print(' Your bucket %s is successfully created ' %your_amazon_bucket)
        print('=' * 60)
        print()
        time.sleep(1)
    else:
        bucket = connexion.get_bucket(your_amazon_bucket, validate=True)
        print(" Your Amazon bucket" , your_amazon_bucket ," already exists. " )
    time.sleep(1)


def remove_bucket(your_amazon_bucket, your_aws_access_key_id, your_aws_access_key_secret, your_region_host, ):
    """
    Remove bucket for a given AWS account.

    Parameters
    ----------
    your_amazon_bucket: str
        AWS bucket name.

    your_aws_access_key_id: str
        AWS acces key id.

    your_aws_access_key_secret: str
        AWS key secret.

    your_region_host: str
        Region a given AWS account.your_amazon_bucket: str
        AWS bucket name.
    """
    os.environ['S3_USE_SIGV4'] = 'True'
    session = boto3.Session(your_aws_access_key_id, your_aws_access_key_secret)
    s3 = session.resource(service_name='s3')
    bucket = s3.Bucket(your_amazon_bucket)
    bucket.object_versions.delete()
    bucket.delete()
    print('=' * 60)
    print(' Deleting the bucket: %s ... ' %your_amazon_bucket)
    print(' Your bucket %s is successfully deleted ' %your_amazon_bucket)
    print('=' * 60)
    print()
    time.sleep(1)


def backup_to_zip(your_source_directory, your_backup_directory, your_backup_log, your_password):
    """Compress your source directory and protect
    your archive with password.

    Parameters
    ----------
    your_source_directory_path: str

    your_backup_directory_path: str
    """
    your_source_directory_path = Path(your_source_directory)
    your_backup_directory_path = Path(your_backup_directory)
    max_backup = 5
    existing_backups = [
    x for x in your_backup_directory_path.iterdir()
    if x.is_file() and x.suffix == '.zip' and x.name.startswith('Sauvegarde')]
    oldest_to_newest_backup_by_name = list(sorted(existing_backups, key=lambda f: f.name))

    while len(oldest_to_newest_backup_by_name) >= max_backup:
        backup_to_delete = oldest_to_newest_backup_by_name.pop(0)
        backup_to_delete.unlink()
        print('=' * 60)
        print(' Deleting old backups... ')
        print('=' * 60)
        time.sleep(1)
    message_start = " Local backup is starting... ".center(60, '=')
    print(message_start)
    print('=' * 60)
    backup_file_name = f'Sauvegarde du dossier {your_source_directory_path.name} du {datetime.now().strftime("%d-%m-%Y à %H%M%S")}.zip'
    zf = pyzipper.AESZipFile((your_backup_directory_path / backup_file_name), mode='w', compression = pyzipper.ZIP_LZMA, encryption = pyzipper.WZ_AES)
    zf.pwd = your_password.encode()
    if your_source_directory_path.is_file():
    # File backup
        zf.write(
        your_source_directory_path,
        arcname=your_source_directory_path.name,
        compress_type=pyzipper.ZIP_LZMA)
    elif your_source_directory_path.is_dir():
    # Directory backup
        for file in your_source_directory_path.glob('**/*'):
            if file.is_file():
                zf.write(
                file.absolute(),
                arcname=str(file.relative_to(your_source_directory_path)),
                compress_type=pyzipper.ZIP_LZMA)
    # Zip processus end
        zf.close()
    if not os.path.exists(your_backup_log):
        with open(your_backup_log, 'w') as f:
            f.write(' %s: info: Backup completed successfully \n'%(datetime.now().strftime("%d-%m-%Y à %H%M%S")))
    time.sleep(1)
    print('=' * 60)
    print(' \n Backup completed successfully \n Backup stored in %s \n' %(your_backup_directory))
    print('=' * 60)
    message_end = " Local backup terminated with success. ".center(60,'=')
    print(message_end)
    print('=' * 60)


def upload_to_aws(your_backup_directory,your_backup_log, your_amazon_bucket, your_aws_access_key_id, your_aws_access_key_secret, your_region_host):
    """
    Upload directory on AWS S3 bucket.

    Parameters
    ----------
    your_amazon_bucket: str
        AWS bucket name.

    your_aws_access_key_id: str
        AWS acces key id.

    your_aws_access_key_secret: str
        AWS key secret.

    your_region_host: str
        Region a given AWS account.your_amazon_bucket: str
        AWS bucket name.
    """
    message_start = " Amazon S3 backup is starting... ".center(60, '=')
    print(message_start)
    print('=' * 60)

    os.environ['S3_USE_SIGV4'] = 'True'
    connexion = boto.connect_s3(
        your_aws_access_key_id,
        your_aws_access_key_secret,
        host=your_region_host
    )
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
                    fname=os.path.join(root,name)
                    upload_file_names.append(fname)
                    print (upload_file_names)

            for filenames in upload_file_names:
                filename=filenames.replace("\\", "/")
                sourcepath = filename
                destpath = filename

                k = boto.s3.key.Key(bucket)
                k.key = destpath
                k.set_contents_from_filename(sourcepath)
                f = open(your_backup_log,'a')
                f.write(' %s: info: Amazon S3 Upload completed successfully \n'%(datetime.now().strftime("%d-%m-%Y à %H%M%S")))
                f.close()
                print(" Upload Successful ".center(60,'='))
                message_end = " Amazon S3 backup terminated with success ".center(60,'=')
                print(message_end)
                print('=' * 60)
                return True
        except FileNotFoundError:
            print("The file was not found")
            return False

def mailer(your_email_address, your_psw,your_backup_log):
    """
    This function sends an email to user with log file.

    Parameters
    ----------
    your_email_address: str
        email address where backup.log will be send.
    your_psw: str
        email password.
    """
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
