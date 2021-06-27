![Python](https://img.shields.io/badge/python-3.9.5-red) ![LicenseMIT](https://img.shields.io/badge/license-MIT-brightgreen) ![Version](https://img.shields.io/badge/version-1.0-orange) 

# s3_backup_tool



     _______. ____      .______        ___        ______  __  ___  __    __  .______      .___________.  ______     ______    __      
    /       ||___ \     |   _  \      /   \      /      ||  |/  / |  |  |  | |   _  \     |           | /  __  \   /  __  \  |  |     
   |   (----`  __) |    |  |_)  |    /  ^  \    |  ,----'|  '  /  |  |  |  | |  |_)  |    `---|  |----`|  |  |  | |  |  |  | |  |     
    \   \     |__ <     |   _  <    /  /_\  \   |  |     |    <   |  |  |  | |   ___/         |  |     |  |  |  | |  |  |  | |  |     
.----)   |    ___) |    |  |_)  |  /  _____  \  |  `----.|  .  \  |  `--'  | |  |             |  |     |  `--'  | |  `--'  | |  `----.
|_______/    |____/     |______/  /__/     \__\  \______||__|\__\  \______/  | _|             |__|      \______/   \______/  |_______|
                                                                                                                                      




## About.



This is a simple backup script written in Python 3 and that offers a generic way to backup locally files or directories and to upload backups on Amazon Web Service S3.


## How to install?

Install the last version of Python : https://www.python.org/ .

s3_backup_tool needs Boto and many dependencies to be installed on your system.

pip install boto


The script requires your AWS credentials :

    Access Key ID 
    Access Key Secret
    Region host


## How does it work?

![Launcher](/image/Sans%20titre.png?raw=true)

Option 1 : allows you to create if you need your source directory to backup.

Option 2 : allows you to create your target directory at the desired location.

Option 3 : allows you to listed all the buckets on you Amazon S3 Service.

Option 4/5 : allows tou to create and/or remove bucket on you Amazon S3 Service.

Option 6 : this step copies files or directories and puts everything in a single .zip file protectd by password. You can choose source file/directory, and source                backup directory. The script checks for each execution, the existence of the source and destination folders.
           Once everything is ready, let's upload the files to your Amazon S3 bucket.
           
Option 7 : allows you to upload file/folder on your Amazon S3 Service


## How to schedule automatic script execution?

• If you have Windows: https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page

• If you have Linux or Mac: https://www.howtogeek.com/101288/how-to-schedule-tasks-on-linux-an-introduction-to-crontab-files/


## Contribution guidelines.



If you have any idea or suggestion contact directly the Repo Owner.


## License.



This project is licensed under the MIT License. Please see the LICENSE file for complete license text.

