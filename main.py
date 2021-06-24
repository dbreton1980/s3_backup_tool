from utils import menu, source_directory, backup_directory, deleting_old_backups, backup_to_zip, upload_to_aws, mailer

if __name__ == '__main__':
    menu()
    source_directory()
    backup_directory()
    deleting_old_backups()
    backup_to_zip()
    upload_to_aws()
    mailer()