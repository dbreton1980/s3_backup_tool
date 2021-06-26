[Python](https://img.shields.io/badge/python-3.9.5-red) [LicenseMIT](https://img.shields.io/badge/license-MIT-brightgreen) [Version](https://img.shields.io/badge/version-1.0-orange) 
**
# s3_backup_tool

**
**

## About.

**

This is a simple backup script written in Python 3 and that offers a generic way to backup locally files or directories and to upload backups on Amazon Web Service S3.
**

## How to install?

**

Install the last version of Python : https://www.python.org/ .

s3_backup_tool needs Boto3 and many dependencies to be installed on your system.
**

## How does it work?

**
![Launcher](https://github.com/dbreton1980/s3_backup_tool/tree/master/image/Sans%20titre.png)
There are two customizable steps in this process:

• Backup. This step copies files or directories and puts everything in a single .zip file protectd by password. You can choose source file/directory, and source backup directory. The script checks for each execution, the existence of the source and destination folders.

• Upload on Amazon S3. Once everything is ready, let's upload the files to your Amazon S3 bucket.

You can also create, remove or listed buckets on Amazon S3 Service
**

## How to schedule automatic script execution?

**

• If you have Windows: https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page

• If you have Linux or Mac: https://www.howtogeek.com/101288/how-to-schedule-tasks-on-linux-an-introduction-to-crontab-files/
**

## Contribution guidelines.

**

If you have any idea or suggestion contact directly the Repo Owner.
**

## License.

**

This project is licensed under the MIT License. Please see the LICENSE file for complete license text.

