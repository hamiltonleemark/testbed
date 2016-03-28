.. _QuickStartAnchor:

Quick Start
===============

Testbed can be installed in a standalone manner in order to demonstrate several key concepts. Standalone mode is functionaly rich and useful for evaluating testbed.

Here are the required steps to setup the development environment.

#. Install several requried packages:

  **sudo apt-get install python-pip python-yaml libmysqlclient-dev python-dev**
#. Install testbed from the github release area:

  **sudo pip install https://github.com/testbed/testbed/archive/v0.1-alpha.9.tar.gz**
#. Create local temporary database

  **tbd-manage migrate**
#. Validate proper configuration. confirm all checks pass.

   **tbd db check**
