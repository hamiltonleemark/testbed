.. _InstallationAnchor:

Installation
************

Getting Testbed
===============

If you want the latest code you'll need a `GitHub <http://www.github.com/>`_ account. This is also where we track issues and feature ideas. 

What is Installed
=================

Testbed is fundamentally a client server application which relies on a 
database for **normal** operation. A database and testbed software is 
installed on a single machine. All clients install testbed then configured 
with the location of the database.

Ubuntu 14.04
------------

Here are the required steps to setup testbed on both client and server for
Ubuntu 14.04.

#. sudo apt-get install python-pip python-yaml
#. git 
#. sudo pip install -r requirements.txt

On the server, the following additional steps are required:
 Apache2 configuration on Ubuntu14.04
sudo apt-get install apache2 libapache2-mod-wsgi

sudo ln -s /etc/apache2/sites-available/testbed.conf /etc/apache2/sites-enabled/testbed.conf
