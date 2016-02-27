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

Here are the required steps to setup testbed on both client and server for
Ubuntu 14.04.

#. sudo apt-get install python-pip python-yaml
#. git clone git@github.com:testbed/testbed.git
#. cd testbed
#. sudo pip install -r requirements.txt

Server Installation on Ubuntu 14.04
-----------------------------------
On the server, folow these steps:
#.  sudo apt-get install apache2 libapache2-mod-wsgi
cd  testbed
sudo ln -s /etc/apache2/sites-available/testbed.conf /etc/apache2/sites-enabled/testbed.conf
