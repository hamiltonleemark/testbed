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

Server Installation on Ubuntu 14.04
-----------------------------------

Here are the steps for installing testbed on a server, a mysql database must be setup by following these steps:

#. Install several packages 
   **sudo apt-get install python-pip python-yaml libmysqlclient-dev python-dev**
   **sudo apt-get install apache2 libapache2-mod-wsgi**
#. Install mysql server, **sudo apt-get install mysql-server-5.5**. During thie step you'll be asked to set the mysql root password. Remember this value for 
later. Normally this account is not used for general access to the mysql
server. Later a mysql account called **testbed** will be created to 
provide access to the testbed specific content.
#. Install latest testbed
   **sudo pip install https://github.com/testbed/testbed/archive/v0.1-alpha.8.tar.gz**
#. Add testbed configuration 
   **sudo cp /usr/local/testbed/apache2/sites-available/testbed.conf  /etc/apache2/sites-available/testbed.conf**
#. Enable testbed apache configuration,
   sudo ln -s /etc/apache2/sites-available/testbed.conf /etc/apache2/sites-enabled/testbed.conf
#. Restart the apache server, **sudo service apache2 restart**
#. Assuming the default user "testbed", create this user in mysql:
   mysql -u root -p -e "CREATE USER 'testbed'@'%' IDENTIFIED BY 'password';"
   mysql -u root -p -e "GRANT ALL PRIVILEGES ON * . * TO 'testbed'@'%';"
   mysql -u root -p -e "FLUSH PRIVILEGES;"
   Any user name and password can be used. This information simply needs to 
   be provided in the final step when mysql.cnf is created. By default, **testbed** and **password** credentials are assumed.
#. On the server, create the testbed database. Usually this is done with
   the root account:
   mysql -u root -p -e "create database testbed;"
#. Create database and admin account. During this step provide a username 
   and password. This is an account that will be used to log into the website
   with administrative priveleges.
   /usr/local/bin/tbd-manage syncdb
#. Edit **/usr/local/testbed/etc/mysql.cnf** and change the password which was 
   set in the previous step.

Client Installation on Ubuntu 14.04
-----------------------------------

Here are the steps to setup testbed on both a client running Ubuntu 14.04.
Versions are currently available through github.com on
https://github.com/testbed/testbed/releases. Please look through the 
release site to find the latest version. The example below uses an older
version:

#. sudo apt-get install python-pip python-yaml libmysqlclient-dev python-dev
#. sudo pip install https://github.com/testbed/testbed/archive/v0.1-alpha.8.tar.gz
#. Create or edit the file **/usr/local/testbed/etc/mysql.cnf** with the 
   location of the testbed server.  
