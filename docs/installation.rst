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

Here are the required steps to setup testbed on both a client and a server for
Ubuntu 14.04. Versions are currently available through github.com on
https://github.com/testbed/testbed/releases. The instructions below use 
v0.1-alpha.1 as example.

#. sudo apt-get install python-pip python-yaml
#. sudo pip install --upgrade https://github.com/testbed/testbed/archive/v0.1-alpha.1.tar.gz
#. Create or edit the file **/usr/local/testbed/etc/mysql.cnf** with the 
   location of the testbed server.  

Server Installation on Ubuntu 14.04
-----------------------------------

Additionally on a server, a mysql database must be setup by following these
steps:

#. sudo apt-get install apache2 libapache2-mod-wsgi
#. cp examples/etc/apache2/sites-available/testbed.conf /etc/apache2/sites-available/testbed.conf
#. sudo ln -s /etc/apache2/sites-available/testbed.conf /etc/apache2/sites-enabled/testbed.conf
