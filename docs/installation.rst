.. _InstallationAnchor:

Installation
************

Getting Testbed
===============

If you want the latest code you'll need a `GitHub <http://www.github.com/>`_ account. This is also where we track issues and feature ideas. 

What is Installed
=================

Testbed is fundamentally a client server application which relies on a 
database for **normal** operation. The database requires a testbed 
installation as well as configuring the database. Client only need to install 
the testbed software. For evaluation purposes a single system can be used.

Client Installation on Ubuntu 14.04
-----------------------------------

Here are the steps to setup testbed on both a client running Ubuntu 14.04.
Versions are currently available through github.com on
https://github.com/testbed/testbed/releases. Please look through the 
release site to find the latest version. The example below uses an older
version:

#. sudo apt-get install python-pip python-yaml libmysqlclient-dev python-dev
#. sudo pip install https://github.com/testbed/testbed/archive/v0.1-alpha.3.tar.gz
#. Create or edit the file **/usr/local/testbed/etc/mysql.cnf** with the 
   location of the testbed server.  

Server Installation on Ubuntu 14.04
-----------------------------------

Here are the steps for installing testbed on a server, a mysql database must be setup by following these steps:

#. sudo apt-get install python-pip python-yaml libmysqlclient-dev python-dev
#. sudo apt-get install apache2 libapache2-mod-wsgi
#. Install mysql server, **sudo apt-get install mysql-server-5.5.**. During thie step you'll be asked to set the root password. Remember thie value for later.
#. sudo pip install https://github.com/testbed/testbed/archive/v0.1-alpha.3.tar.gz
#. Edit **/usr/local/testbed/etc/mysql.cnf** change the password which was set in step 4.
#. Add testbed configuration 
   sudo cp /usr/local/testbed/etc/apache2/sites-available/testbed.conf  /etc/apache2/sites-available/testbed.conf
#. Enable testbed apache configuration,
   sudo ln -s /etc/apache2/sites-available/testbed.conf /etc/apache2/sites-enabled/testbed.conf
#. On the server, create the testbed database. Usually this is done with
   the root account:
   mysql -u root -p -e "create database testbed;"
#. Assuming the default user "testbed", create this user in mysql:
   CREATE USER 'testbed'@'%' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON * . * TO "testbed"@"%";
   FLUSH PRIVILEGES;
#. Restart apache2
   sudo service apache2 restart
