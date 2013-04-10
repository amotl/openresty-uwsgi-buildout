==================
OpenResty Buildout
==================


Installation
============
Simply run these commands for installation::

    python bootstrap.py -v 1.7.0
    bin/buildout

Fire up both the uwsgi and the nginx servers in different consoles::

    bin/uwsgi --xml parts/uwsgi/uwsgi.xml
    bin/nginx-nodaemon


Configuration
=============

Nginx
-----
To reconfigure Nginx, simply edit the file located in
``templates/etc/nginx.conf.in`` and run the following command::
    
    bin/buildout install templates

Buildout
--------
To reconfigure the buildout infrastructure, see ``buildout.cfg``,
``openresty.cfg``, ``uwsgi.cfg`` and ``versions.cfg``.
