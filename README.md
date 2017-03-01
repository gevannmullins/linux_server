# linux_server
Udacity course - Linux Server Configurations

Instructions:

1. Create a new GitHub repository and add a file named README.md. ----- done
2. Your README.md file should include all of the following:
   i. The IP address and SSH port so your server can be accessed by the reviewer.
        IpAddress: 52.41.212.50
        Port: 2200
        
   ii. The complete URL to your hosted web application.
        Url: http://52.41.212.50
        
   iii. A summary of software you installed and configuration changes made.
        - Installed Apache Server
        - Installed mod_wsgi
        - Installed PostgreSQL
        - Installed git
        - Installed Flask
        - Installed SQLAlchemy
        - Installed PIP (for installing Python libraries)
        - Installed oauth2client
        - Installed psycopg2
        - Installed requests
        - Installed httplib2
        
   iv. A list of any third-party resources you made use of to complete this project.
        
   
3. Locate the SSH key you created for the grader user.
4. During the submission process, paste the contents of the grader user's SSH key into the "Notes to Reviewer" field.




These are the steps that I have done to meet the requirements of this project:

Create a new user named grader

root:~$ adduser grader
Give the grader user permission to sudo

root:~$ echo "grader ALL=(ALL) ALL" > /etc/sudoers.d/grader
Without "NOPASSWD" in the config, the user is prompted for password whenever sudo is used.

Set up key-based authentication for grader

A private key (.rsa) and a public key (.pub) were created.

Then I got into the Udacity remote machine and copied contents of public key (.pub file) to /home/grader/.ssh/authorized_keys

root:~$ sudo -i -u grader
grader:~$ mkdir ~/.ssh
grader:~$ vim ~/.ssh/authorized_keys
(copied contents of .pub file into this file)
grader:~$ chmod 700 ~/.ssh
grader:~$ chmod 644 ~/.ssh/authorized_keys
Disable remote SSH login as root

#set this in /etc/ssh/sshd_config
PermitRootLogin no
Disable password-based authentication for SSH

#set this in /etc/ssh/sshd_config
PasswordAuthentication no
Change the SSH port from 22 to 2200

#set this in /etc/ssh/sshd_config
Port 2200
With all the SSH config settings done, I restarted the SSH service:

grader:~$ sudo service ssh restart
I then logged out.

After all these changes so far, to login as grader with private key, I now use:

vagrant:~$ ssh -i ~/.ssh/myprivatekey.rsa grader@54.200.104.8 -p 2200
To check the current SSH port number, I used:

grader:~$ netstat -an | grep ESTABLISHED
There is a tcp entry with ESTABLISHED state that has local address with port 2200.

Update all currently installed packages

grader:~$ sudo apt-get update
grader:~$ sudo apt-get upgrade
I got a "sudo: unable to resolve host ip-10-20-30-114" error every time I used sudo, so I added that hostname to /etc/hosts:

#added this line to /etc/hosts
127.0.1.1 ip-10-20-30-114
After exiting and logging back in via ssh, I got a "***system restart is required***" message, so I rebooted the system:

grader:~$ sudo reboot
Configure the Uncomplicated Firewall (UWF) to only allow incoming connections for SSH (port 2200), HTTP (port 80) and NTP (port 123)

grader:~$ sudo ufw default deny incoming
Default incoming policy changed to 'deny'
grader:~$ sudo ufw default allow outgoing
Default outgoing policy changed to 'allow'
grader:~$ sudo ufw allow 2200
Rules updated
Rules updated (v6)
grader:~$ sudo ufw allow www
Rules updated
Rules updated (v6)
grader:~$ sudo ufw allow ntp
Rules updated
Rules updated (v6)
grader:~$ sudo ufw enable
I then checked that the desired ports are opened:

grader:~$ sudo ufw status
Status: active

To              Action  From
--              ------  ----
80/tcp          ALLOW   Anywhere
2200            ALLOW   Anywhere
123             ALLOW   Anywhere
80/tcp (v6)     ALLOW   Anywhere (v6)
2200 (v6)       ALLOW   Anywhere (v6)
123 (v6)        ALLOW   Anywhere (v6)   
I also tried logging out of the Udacity remote machine and ssh using default port 22 but no connection can be made.

Configure the local timezone to UTC

When I ran the date command, it shows the time in UTC, so I didn't make any changes here.

Install and configure Apache to serve a Python mod_wsgi application

Installed Apache:

grader:~$ sudo apt-get install apache2
At this point of time, I was able to visit http://54.200.104.8/ to see the Apache2 Ubuntu Default Page.

Installed mod_wsgi:

grader:~$ sudo apt-get install libapache2-mod-wsgi
Got an error message that says: "apache2: Could not reliably determine the server's fully qualified domain name, using 127.0.0.1. Set the 'ServerName' directive globally to suppress this message". So I added the line below to /etc/apache2/apache2.conf:

ServerName localhost
Install and configure PostgreSQL

grader:~$ sudo apt-get install postgresql
Created a new user named catalog that has limited permissions to the catalog application database

grader:~$ sudo adduser catalog  

grader:~$ sudo -i -u postgres
postgres:~$ createuser --interactive -P
Enter name of role to add: catalog
Enter password for new role:
Enter it again:
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create database? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n

postgres:~$ psql
postgres=# CREATE DATABASE catalog;
postgres=# \q

postgres:~$ exit
logout
grader:~$   
Install git, clone and setup your Catalog App project so that it functions correctly when visiting your server's IP address in a browser.

First, I installed Git:

grader:~$ sudo apt-get install git
I cloned the Item Catalog project using git:

grader$ sudo mkdir -p /var/www/itemcatalog/ItemCatalog
grader$ sudo git clone https://github.com/shikeyou/ItemCatalog.git /var/www/itemcatalog/ItemCatalog
Protected .git folder:

grader$ sudo chmod 700 /var/www/itemcatalog/ItemCatalog/.git
I added http://54.200.104.8 to Authorized JavaScript Origins in the project in Google Developer Console, then downloaded the JSON file. Copied the JSON file contents to a new file /var/www/itemcatalog/ItemCatalog/client_secrets.json.

Installed additional packages and libraries necessary to host this application:

grader:~$ sudo apt-get install python-psycopg2
grader:~$ sudo apt-get install python-flask
grader:~$ sudo apt-get install python-sqlalchemy
grader:~$ sudo apt-get install python-pip
grader:~$ sudo pip install oauth2client
grader:~$ sudo pip install requests
grader:~$ sudo pip install httplib2
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
app = Flask(__name__)
app.secret_key = os.urandom(123)  #move this out of the "if __name__ == '__main__'" block 

