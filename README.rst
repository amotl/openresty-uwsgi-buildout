==============
NGINX Buildout
==============

Installation
============

Simply run this commands for the installation::

    python bootstrap.py
    bin/buildout -vvN

Configuration
=============

To configure the nginx, simply edit the file located in
``templates/etc/nginx.conf.in`` and run the following command::
    
    bin/buildout -vvN install templates

