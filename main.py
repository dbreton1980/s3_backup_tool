import sys
import time
import smtplib
import pyzipper
import boto3

from getpass import getpass
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from pathlib import Path

from utils import get_menu_choice, backup_directory, list_bucket


if __name__ == '__main__':

    choice = get_menu_choice()

    if choice == '1':
        time.sleep(1)
        your_backup_directory = input(" Enter your backup directory path: ")
        print(' You said: %s' % your_backup_directory)
        yes_no = input(" Do you want to continue? Enter yes/no: ")
        yes_choice = ['yes', 'y', 'ye', 'Y']
        no_choice = ['no', 'n', 'N']
        if yes_no in yes_choice:
            backup_directory(your_backup_directory)

    elif choice == '2':
        time.sleep(1)
        your_aws_access_key_id = input(" Enter your AWS_ACCESS_KEY_ID: ")
        your_aws_access_key_secret = input(" Enter your AWS_ACCESS_KEY_SECRET: ")
        your_region_host = input(" Enter your REGION_HOST: ")
        print(' You said: %s' % your_region_host)
        os.environ['S3_USE_SIGV4'] = 'True'
        yes_no = input(" Do you want to display the contents of S3 for the current account ? Enter yes/no: ")
        yes_choice = ['yes', 'y', 'ye', 'Y']
        no_choice = ['no', 'n', 'N']
        if yes_no in yes_choice:
            list_bucket(your_aws_access_key_id, your_aws_access_key_secret)
        elif yes_no in no_choice:
            choice = get_menu_choice()

    elif choice == '3':
        time.sleep(1)
        your_amazon_bucket = input(" Enter your amazon bucket name: ")
        print(' You said: %s' % your_amazon_bucket)
        your_aws_access_key_id = input(" Enter your AWS_ACCESS_KEY_ID: ")
        your_aws_access_key_secret = input(" Enter your AWS_ACCESS_KEY_SECRET: ")
        your_region_host = input(" Enter your REGION_HOST: ")
        print(' You said: %s' % your_region_host)
        os.environ['S3_USE_SIGV4'] = 'True'
        yes_no = input(" Do you want to continue? Enter yes/no: ")
        yes_choice = ['yes', 'y', 'ye', 'Y']
        no_choice = ['no', 'n', 'N']
        if yes_no in yes_choice:
            create_bucket(your_amazon_bucket)
        if yes_no in no_choice:
            menu()

    elif choice == '4':
        time.sleep(1)
        your_amazon_bucket = input(" Enter your amazon bucket name: ")
        print(' You said: %s' % your_amazon_bucket)
        your_aws_access_key_id = input(" Enter your AWS_ACCESS_KEY_ID: ")
        your_aws_access_key_secret = input(" Enter your AWS_ACCESS_KEY_SECRET: ")
        your_region_host = input(" Enter your REGION_HOST: ")
        print(' You said: %s' % your_region_host)
        os.environ['S3_USE_SIGV4'] = 'True'
        yes_no = input(" Are you sure you want to remove this bucket ? Enter yes/no: ")
        yes_choice = ['yes', 'y', 'ye', 'Y']
        no_choice = ['no', 'n', 'N']
        if yes_no in yes_choice:
            def remove_bucket():
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
                menu()
            if __name__ == '__main__':
                remove_bucket()
        if yes_no in no_choice:
            menu()

    elif choice == '5':
        time.sleep(1)
        print('=' * 60)
        print(' Beginning the local backup process ... ')
        print('=' * 60)
        your_source_directory = input(" Enter your source directory path: ")
        print(' You said: %s' % your_source_directory)
        your_backup_directory = input(" Enter your backup directory path: ")
        print(' You said: %s' % your_backup_directory)
        your_backup_log = input(" Enter your backup log path: ")
        print(' You said: %s' % your_backup_log)
        your_email_address = input(" Enter your email address: ")
        print('You said: %s' % your_email_address)
        your_psw = getpass(prompt=' Enter your email password: ')
        your_amazon_bucket = input(" Enter your amazon bucket name: ")
        print('You said: %s' % your_amazon_bucket)
        your_aws_access_key_id = input("Enter your AWS_ACCESS_KEY_ID: ")
        your_aws_access_key_secret = input(" Enter your AWS_ACCESS_KEY_SECRET: ")
        your_region_host = input(" Enter your REGION_HOST:")
        print('You said: %s' % your_region_host)
        os.environ['S3_USE_SIGV4'] = 'True'
        your_source_directory_path = Path(your_source_directory)
        your_backup_directory_path = Path(your_backup_directory)
        your_password = getpass(prompt=' Enter your password to protect your archive: ')
        yes_no = input(" Are you sure you want to backup this directory ? Enter yes/no: ")
        yes_choice = ['yes', 'y', 'ye', 'Y']
        no_choice = ['no', 'n', 'N']
        if yes_no in yes_choice:
            #################################################################################################
            #
            #                              LOCAL BACKUP
            #
            #################################################################################################
            message_start = " Local backup is starting... ".center(50, '=')
            print(message_start)

            def source_directory():
                """Check if source directory exist, if don't exists, create it."""
                print('  \n Checking for source directory ... %s  ' %your_source_directory)
                time.sleep(1)
                try:
                    os.makedirs(your_source_directory)
                    print("  Directory " , your_source_directory ,  " created. ")
                except FileExistsError:
                    print("  Directory " , your_source_directory ,  " already exists. ")

            if __name__ == '__main__':
                source_directory()

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
                        os.mkdir(your_backup_directory)
                        if not os.path.exists('your_backup_log'):
                            os.mknod('your_backup_log')
                        else:
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

            if __name__ == '__main__':
                backup_directory()

            def backup_to_zip():
                """Zip your source directory."""
                max_backup = 5
                existing_backups = [
                x for x in your_backup_directory_path.iterdir()
                if x.is_file() and x.suffix == '.zip' and x.name.startswith('Sauvegarde')]
                oldest_to_newest_backup_by_name = list(sorted(existing_backups, key=lambda f: f.name))

                while len(oldest_to_newest_backup_by_name) >= max_backup:
                    backup_to_delete = oldest_to_newest_backup_by_name.pop(0)
                    backup_to_delete.unlink()
                    print(' Deleting old backups... ')
                    time.sleep(1)

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
                f = open(your_backup_log,'a')
                f.write(' %s: info: Backup completed successfully \n'%(datetime.now().strftime("%d-%m-%Y à %H%M%S")))
                f.close()
            time.sleep(1)
            print('=' * 60)
            print(' \n Backup completed successfully \n Backup stored in %s \n' %(your_backup_directory))
            print('=' * 60)

            if __name__ == '__main__':
                backup_to_zip()

            message_end = " Local backup terminated with success. ".center(60,'=')
            print(message_end)

            #################################################################################################
            #
            #                              AMAZON S3 BACKUP
            #
            #################################################################################################

            message_start = " Amazon S3 backup is starting... ".center(60, '=')
            print(message_start)

            def percent_cb(complete, total):
                """Progress point."""
                sys.stdout.write('.')
                sys.stdout.flush()

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
                        k.set_contents_from_filename(sourcepath,cb=percent_cb, num_cb=10)
                        print("Upload Successful")
                        return True

                except FileNotFoundError:
                    print("The file was not found")
                    return False

            if __name__ == '__main__':
                upload_to_aws()
            message_end = " Amazon S3 backup terminated with success ".center(60,'=')
            print(message_end)

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

            if __name__ == '__main__':
                mailer()
        if yes_no in no_choice:
            menu()

    elif choice == '6':
        time.sleep(1)
        print(' Beginning the upload on Amazon S3 ... ')
        your_backup_directory = input(" Enter your backup directory path: ")
        print(' You said: %s' % your_backup_directory)
        your_backup_log = input(" Enter your backup log path: ")
        print(' You said: %s' % your_backup_log)
        your_amazon_bucket = input(" Enter your amazon bucket name:")
        print('You said: %s' % your_amazon_bucket)
        your_aws_access_key_id = input(" Enter your AWS_ACCESS_KEY_ID:")
        your_aws_access_key_secret = input(" Enter your AWS_ACCESS_KEY_SECRET:")
        your_region_host = input(" Enter your REGION_HOST:")
        print(' You said: %s' % your_region_host)
        os.environ['S3_USE_SIGV4'] = 'True'
        yes_no = input(" Are you sure you want to upload this directory ? Enter yes/no: ")
        yes_choice = ['yes', 'y', 'ye', 'Y']
        no_choice = ['no', 'n', 'N']
        if yes_no in yes_choice:
            print('=' * 60)
            message_start = " Amazon S3 backup is starting... ".center(60, '=')
            print(message_start)
            print('=' * 60)
            print()
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
                        k.set_contents_from_filename(sourcepath)
                        print("Upload Successful")
                        return True
                except FileNotFoundError:
                    print("The file was not found")
                    return False
            if __name__ == '__main__':
                upload_to_aws()
            print('=' * 60)
            message_end = " Amazon S3 backup terminated with success ".center(60,'=')
            print(message_end)
            print('=' * 60)
        if yes_no in no_choice:
            menu()

    elif choice == 'h':
        print(' "your_source_directory", "Specify the directory to backup (SOURCE)." ')
        print(' "your_backup_directory", "Specify the directory where the backup should be stored (TARGET)." ')
        print(' "your_backup_log", "Specify the directory where the backup should be stored." ')
        print(' "your_email_address", "eMail-Adress where to send the backup log." ')
        menu()
    else:
        print(' Invalid choice. ')
        time.sleep(1)
        menu()


    elif choice == '5':
        choices = get_all_choices()
        backup_directory(choices['your_backup_directory_path'])
