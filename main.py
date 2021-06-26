from utils import get_all_choices, get_menu_choice, source_directory, backup_directory, list_bucket, create_bucket, remove_bucket, backup_to_zip, upload_to_aws, mailer
from utils import time

if __name__ == '__main__':

    choice = get_menu_choice()

    if choice == '1':
        time.sleep(1)
        your_source_directory = input(" Enter your source directory path: ")
        print(' You said: %s' % your_source_directory)
        yes_no = input(" Do you want to continue? Enter yes/no: ")
        yes_choice = ['yes', 'y', 'ye', 'Y']
        no_choice = ['no', 'n', 'N']
        if yes_no in yes_choice:
            source_directory(your_source_directory)
        elif yes_no in no_choice:
            choice = get_menu_choice()

    elif choice == '2':
        time.sleep(1)
        your_backup_directory = input(" Enter your backup directory path: ")
        print(' You said: %s' % your_backup_directory)
        yes_no = input(" Do you want to continue? Enter yes/no: ")
        yes_choice = ['yes', 'y', 'ye', 'Y']
        no_choice = ['no', 'n', 'N']
        if yes_no in yes_choice:
            backup_directory(your_backup_directory)
        elif yes_no in no_choice:
            choice = get_menu_choice()

    elif choice == '3':
        time.sleep(1)
        your_aws_access_key_id = input(" Enter your AWS_ACCESS_KEY_ID: ")
        your_aws_access_key_secret = input(" Enter your AWS_ACCESS_KEY_SECRET: ")
        your_region_host = input(" Enter your REGION_HOST: ")
        print(' You said: %s' % your_region_host)
        yes_no = input(" Do you want to display the contents of S3 for the current account ? Enter yes/no: ")
        yes_choice = ['yes', 'y', 'ye', 'Y']
        no_choice = ['no', 'n', 'N']
        if yes_no in yes_choice:
            list_bucket(your_aws_access_key_id, your_aws_access_key_secret, your_region_host)
        elif yes_no in no_choice:
            choice = get_menu_choice()

    elif choice == '4':
        time.sleep(1)
        your_amazon_bucket = input(" Enter your amazon bucket name: ")
        print(' You said: %s' % your_amazon_bucket)
        your_aws_access_key_id = input(" Enter your AWS_ACCESS_KEY_ID: ")
        your_aws_access_key_secret = input(" Enter your AWS_ACCESS_KEY_SECRET: ")
        your_region_host = input(" Enter your REGION_HOST: ")
        print(' You said: %s' % your_region_host)
        yes_no = input(" Do you want to continue? Enter yes/no: ")
        yes_choice = ['yes', 'y', 'ye', 'Y']
        no_choice = ['no', 'n', 'N']
        if yes_no in yes_choice:
            create_bucket(your_amazon_bucket, your_aws_access_key_id, your_aws_access_key_secret, your_region_host)
        elif yes_no in no_choice:
            choice = get_menu_choice()

    elif choice == '5':
        time.sleep(1)
        your_amazon_bucket = input(" Enter your amazon bucket name: ")
        print(' You said: %s' % your_amazon_bucket)
        your_aws_access_key_id = input(" Enter your AWS_ACCESS_KEY_ID: ")
        your_aws_access_key_secret = input(" Enter your AWS_ACCESS_KEY_SECRET: ")
        your_region_host = input(" Enter your REGION_HOST: ")
        print(' You said: %s' % your_region_host)
        yes_no = input(" Are you sure you want to remove this bucket ? Enter yes/no: ")
        yes_choice = ['yes', 'y', 'ye', 'Y']
        no_choice = ['no', 'n', 'N']
        if yes_no in yes_choice:
            remove_bucket(your_amazon_bucket, your_aws_access_key_id, your_aws_access_key_secret, your_region_host)
        elif yes_no in no_choice:
            choice = get_menu_choice()

    elif choice == '6':
        choices = get_all_choices()
        source_directory(choices['your_source_directory'])
        backup_directory(choices['your_backup_directory'])
        create_bucket(choices['your_amazon_bucket'],choices['your_aws_access_key_id'],choices['your_aws_access_key_secret'],choices['your_region_host'])
        backup_to_zip(choices['your_source_directory'],choices['your_backup_directory'],choices['your_backup_log'],choices['your_password'])
        upload_to_aws(choices['your_backup_directory'],choices['your_amazon_bucket'],choices['your_aws_access_key_id'],choices['your_aws_access_key_secret'],choices['your_region_host'])
        mailer(choices['your_email_address'],choices['your_psw'],choices['your_backup_log'])

    elif choice == '7':
        time.sleep(1)
        print(' Beginning the upload on Amazon S3 ... ')
        your_backup_directory = input(" Enter your backup directory path: ")
        print(' You said: %s' % your_backup_directory)
        your_backup_log = input(" Enter your backup log path: ")
        print(' You said: %s' % your_backup_log)
        your_amazon_bucket = input(" Enter your amazon bucket name:")
        print(' You said: %s' % your_amazon_bucket)
        your_aws_access_key_id = input(" Enter your AWS_ACCESS_KEY_ID:")
        your_aws_access_key_secret = input(" Enter your AWS_ACCESS_KEY_SECRET:")
        your_region_host = input(" Enter your REGION_HOST:")
        print(' You said: %s' % your_region_host)
        yes_no = input(" Are you sure you want to upload this directory ? Enter yes/no: ")
        yes_choice = ['yes', 'y', 'ye', 'Y']
        no_choice = ['no', 'n', 'N']
        if yes_no in yes_choice:
            upload_to_aws(your_backup_directory, your_backup_log, your_amazon_bucket, your_aws_access_key_id, your_aws_access_key_secret, your_region_host)
        elif yes_no in no_choice:
            choice = get_menu_choice()

    elif choice == 'h':
        print('=' * 60)
        print(' "your_source_directory", "Specify the directory to backup (SOURCE)." ')
        print(' "your_backup_directory", "Specify the directory where the backup should be stored (TARGET)." ')
        print(' "your_backup_log", "Specify the directory where the backup should be stored." ')
        print(' "your_email_address", "eMail-Adress where to send the backup log." ')
        print(' "your_amazon_bucket", ""Specify your AWS bucket name." ')
        print(' "your_aws_access_key_id", "Specify your AWS acces key id." ')
        print(' "your_aws_access_key_secret", "Specify your AWS key secret." ')
        print('=' * 60)
        choice = get_menu_choice()

    elif choice == 'q':
        print(' \n Exiting ... ')
        sys.exit(1)

    else:
        print(' Invalid choice. ')
        time.sleep(1)
        choice = get_menu_choice()
