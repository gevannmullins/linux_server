# Linux Server Configuration

## Udacity course - Linux Server Configurations

The IP address and SSH port so your server can be accessed by the reviewer.
 - IpAddress: 52.37.193.178
 - Port: 2200
    
The complete URL to your hosted web application.
 - Url: http://52.37.193.178

### Instructions:

##### 1. Created Github account:
 - https://github.com/gevannmullins/linux_server.git
 
##### 2. Created new user "grader"
 - $ adduser grader
 - Gave a temporary password - "password"
 
##### 3. Gave "grader" sudo permission
 - $ echo "grader ALL=(ALL) ALL" > /etc/sudoers.d/grader
 
##### 4. Generated ssh-key on my local machine
 - $ ssh-keygen

##### 5. Copied the contents of the ssh public key to "/home/grader/.ssh/authorized_keys"
 - $ sudo grader
 - $ mkdir ~/.ssh
 - $ sudo nano ~/.ssh/authorized_keys

##### 6. Added some permissions to the files
 - $ chmod 700 ~/.ssh
 - $ chmod 644 ~/.ssh/authorized_keys
 
##### 7. Disabled the remote "root" user login. Disabled password-based authentication. Changed the SSH Port from 22 to 2200
 - Made an edit to "/etc/ssh/sshd_config"
    - PermitRootLogin no
    - PasswordAuthentication no
    - Port 2200

##### 8. Restarted SSH Service and logged in as "grader"
 - $ sudo service ssh restart
 - $ ssh -i ~/.ssh/grader grader@52.37.193.178 -p 2200
 
##### 9. Updated all the packages
 - $ sudo apt-get update
 - $ sudo apt-get upgrade
 
##### 10. Removed the annoying error message when running commands by editing the "/etc/hosts" file.
 - 127.0.1.1 ip-10-20-43-164

##### 11. Configured UWF to only allow incoming connections for SSH (port 2200), HTTP (port 80) and NTP (port 123)
 - $ sudo ufw default deny incoming
 - $ sudo ufw default allow outgoing
 - $ sudo ufw allow 2200
 - $ sudo ufw allow www
 - $ sudo ufw allow ntp
 - $ sudo ufw enable
 - $ sudo ufw status

##### 12. Configure the local timezone to UTC
 - The "local timezone" already set to UTC.
 
##### 13. Installed Apache
 - $ sudo apt-get install apache2
 
##### 14. Installed mod_wsgi
 - $ sudo apt-get install libapache2-mod-wsgi
 
##### 15. Install and configure PostgreSQL
 - $ sudo apt-get install postgresql
 - $ sudo adduser catalog
 - $ sudo -i -u postgres
 - postgres:~$ psql
 - postgres=# CREATE DATABASE catalog;
 - postgres=# \q
 - postgres:~$ exit

##### 16. Installed Git and cloned the repo
 - $ sudo apt-get install git
 - $ sudo mkdir -p /var/www/catalog
 - $ sudo git clone https://github.com/gevannmullins/linux_server.git /var/www/catalog
 - $ sudo chmod 700 /var/www/catalog/.git
 
##### 17. Installed additional packages and libraries 
 - $ sudo apt-get install python-psycopg2
 - $ sudo apt-get install python-flask
 - $ sudo apt-get install python-sqlalchemy
 - $ sudo apt-get install python-pip
 - $ sudo pip install oauth2client
 - $ sudo pip install requests
 - $ sudo pip install httplib2

Changed the project to use PostgreSQL database (it was using SQLite originally):
Changed all references to SQLite database to reference PostgreSQL database:

#change argument of all create_engine() calls to use postgresql instead of sqlite
engine = create_engine('postgresql://catalog:password@localhost/catalog')
The above step was done for

/var/www/itemcatalog/ItemCatalog/application.py
/var/www/itemcatalog/ItemCatalog/db/db_populate_test_data.py
/var/www/itemcatalog/ItemCatalog/db/db_setup.py
/var/www/itemcatalog/ItemCatalog/db/db_show_all_data.py
Setup the new PostgreSQL database catalog and populate it with some test data

grader$ python /var/www/itemcatalog/ItemCatalog/db/db_setup.py
grader$ python /var/www/itemcatalog/ItemCatalog/db/db_populate_test_data.py 
Created a wsgi file as the main entry point, for Flask to work with mod_wsgi:

grader:~$ sudo vim /var/www/itemcatalog/itemcatalog.wsgi
In itemcatalog.wsgi:

#insert application path into sys.path so that it can be found
import sys
applicationPath = '/var/www/itemcatalog/ItemCatalog'
if applicationPath not in sys.path:
    sys.path.insert(0, applicationPath)

#also change current working directory to that path
import os
os.chdir(applicationPath)

#import Flask's app as the WSGI-required application object
from application import app as application
Edited /etc/apache2/sites-available/000-default.conf:

#update server admin email to my email so that it will show up in error pages       
ServerAdmin shikeyou@gmail.com

#change document root
DocumentRoot /var/www/itemcatalog

#create a daemon process for user catalog
#this isolates execution env using a normal user account meant just for serving the app
WSGIDaemonProcess itemcatalog user=catalog group=catalog threads=5

#create script alias for wsgi main entry script
WSGIScriptAlias / /var/www/itemcatalog/itemcatalog.wsgi

#create rules for itemcatalog directory
<Directory /var/www/itemcatalog>
    WSGIProcessGroup itemcatalog
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
</Directory>
After changes were made to the config files, I restarted the Apache server:

grader:~$ sudo apache2ctl restart 
During this whole process, if any error pages were served (e.g. 500 Internal Server Error), I would check:

grader:~$ sudo cat /var/log/apache2/error.log
I also added a logging system to my application.py file so that Flask exceptions get logged (if not, Flask exceptions will just show up as 500 Internal Server Error with nothing showing up in Apache's error log!)

Created the log file first for catalog user:

grader:~$ sudo mkdir /var/log/itemcatalog
grader:~$ sudo touch /var/log/itemcatalog/error.log
grader:~$ sudo chown catalog:catalog /var/log/itemcatalog/error.log
grader:~$ sudo chmod 640 /var/log/itemcatalog/error.log
Then in application.py:

#in /var/www/itemcatalog/ItemCatalog/application.py
import logging
fileHandler = logging.FileHandler('/var/log/itemcatalog/error.log')
fileHandler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s; %(levelname)s; %(message)s', '%Y-%m-%d %H:%M:%S')
fileHandler.setFormatter(formatter)
app.logger.addHandler(fileHandler)
I also had to move the secret key variable out of the if __name__ == '__main__' part for Google+ login to work:

#in /var/www/itemcatalog/ItemCatalog/application.py
app = Flask(__name__)
app.secret_key = os.urandom(123)  #move this out of the "if __name__ == '__main__'" block 
With all these done, the server is up and running, and the application can be viewed at http://54.200.104.8/


        
        