.. _QuickStartAnchor:

Quick Start
===============

Testbed can be installed in a standalone manner in order to demonstrate several key concepts. Standalone mode is functionaly rich and useful for evaluating testbed.

Here are the required steps to setup the development environment.

#. Install several requried packages:

  **sudo apt-get install python-pip python-yaml libmysqlclient-dev python-dev**
#. Install testbed from the github release area:

  **sudo pip install https://github.com/testbed/testbed/archive/v0.1-alpha.8.tar.gz**
#. Remove the testbed configuration file which is necessary for the full
   installation.

  **cd /usr/local/testbed/etc; sudo mv mysql.cnf mysql.cnf.old**

  Set host to the IP address of the testbed server. The user and passowrd 
  properties should also be changed appropriately.
#. Validate proper configuration. confirm all checks pass.

   **tbd db check**
