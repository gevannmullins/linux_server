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
 
 
 grader:~$ sudo adduser catalog  
 
 grader:~$ sudo -i -u postgres
 postgres:~$ createuser --interactive -P
 Enter name of role to add: catalog
 Enter password for new role:
 Enter it again:
 Shall the new role be a superuser? (y/n) n
 Shall the new role be allowed to create database? (y/n) n
 Shall the new role be allowed to create more new roles? (y/n) n


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

##### Changed the project to use PostgreSQL database (it was using SQLite originally):
##### Changed all references to SQLite database to reference PostgreSQL database:

##### 18. Ran the database_setyp.py and add_items.py scripts
 - $ python /var/www/catalog/database_setup.py
 - $ python /var/www/catalog/add_items.py
 
##### 19. Created a wsgi file as the main entry point, for Flask to work with mod_wsgi:
 - $ sudo nano /var/www/catalog/catalog.wsgi
 - Added the following content:

        import sys
        applicationPath = '/var/www/catalog'
        if applicationPath not in sys.path:
            sys.path.insert(0, applicationPath)
        
        import os
        os.chdir(applicationPath)
        
        from application import app as application


##### Edited /etc/apache2/sites-available/000-default.conf:

#update server admin email to my email so that it will show up in error pages       
ServerAdmin gevann@responsive.co.za

#change document root
DocumentRoot /var/www/catalog

#create a daemon process for user catalog
#this isolates execution env using a normal user account meant just for serving the app
WSGIDaemonProcess catalog user=catalog group=catalog threads=5

#create script alias for wsgi main entry script
WSGIScriptAlias / /var/www/catalog/catalog.wsgi

#create rules for itemcatalog directory
<Directory /var/www/catalog>
    WSGIProcessGroup catalog
    WSGIApplicationGroup %{GLOBAL}
    Order deny,allow
    Allow from all
</Directory>
After changes were made to the config files, I restarted the Apache server:

#### restart
sudo service apache2 restart

## Go to server app Url:
 - http://52.37.193.178


        
        