import boto
import os
import time
import sys


def get_menu_choice():
    """
    TODO:
    """
    print('=' * 60)
    print(' S3 Backup Tool Script ')
    print(' Dominique BRETON ')
    print('=' * 60)
    print(' 1. Create your backup directory ')
    print(' 2. Display your Amazon S3 bucket list ')
    print(' 3. Create your Amazon S3 bucket ')
    print(' 4. Remove your Amazon S3 bucket ')
    print(' 5. Full backup ')
    print(' 6. Upload on Amazon S3 ')
    print(' h. Help menu  ')
    return input(' \n Enter Selection:  ')


def backup_directory(your_backup_directory):
    """
    Check if backup directory exist, if don't exists, create it.
    """
    print(' \n Checking for backup directory ... %s ' %your_backup_directory)
    if (os.path.exists(your_backup_directory)) and (os.path.isdir(your_backup_directory)):
        print(" Directory " , your_backup_directory ,  " already exists. " )
        time.sleep(1)
    else:
        print(' Backup directory not found ')
        print(' Creating backup directory ... %s ' %your_backup_directory)
        try:
            os.mkdir(your_backup_directory)
            print(' Backup directory successfully created. ')
            time.sleep(1)
        except:
            print(' An error occurred while creating the directory ... ')
            print(' Try creating the directory %s manually and rerun the script ' %(your_backup_directory))
            sys.exit(0)


def list_bucket(your_aws_access_key_id, your_aws_access_key_secret):
    """
    List all buckets for a given aws account.

    Parameters
    ----------
    your_aws_access_key_id: str
        AWS acces key id.

    your_aws_access_key_secret: str
        AWS key secret.
    """
    connexion = boto.connect_s3(
        your_aws_access_key_id,
        your_aws_access_key_secret,
        host=your_region_host
    )
    buckets = connexion.get_all_buckets()
    print('=' * 60)
    for key in buckets:
        print(key.name)
    print('=' * 60)
    time.sleep(1)


def create_bucket(your_amazon_bucket):
    """
    Upload of zip's folder zipped.

    Parameters
    ----------
    """
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
        print(" Bucket" , your_amazon_bucket ,  " already exists. " )
    time.sleep(1)


def get_all_choices():
    """
    TODO:


    Returns
    -------
    choices: dict
        All choices to execute full process.
    """
    choices = {}
    choices['your_aws_access_key_id'] = input(" Enter your AWS_ACCESS_KEY_ID: ")
    choices['your_aws_access_key_secret'] = input(" Enter your AWS_ACCESS_KEY_SECRET: ")

    return choices
