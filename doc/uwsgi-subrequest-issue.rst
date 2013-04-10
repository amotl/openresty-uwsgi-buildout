=============================
uWSGI subrequest method issue
=============================

While switching our Python WSGI Pyramid application stack
to uWSGI behind OpenResty we hit a road block when issuing
subrequests from Lua to the uWSGI application.

The code in ``ngx_http_uwsgi_module.c`` does not seem to honor
the request *method* when being in the context of a subrequest.
Instead, it seems to inherit the request method of the origin
request.

The issue can be reproduced using this buildout environment.
We're using OpenResty 1.2.6.6 (Nginx 1.2.6), however switching
to OpenResty 1.2.7.5 (Nginx 1.2.7) makes no difference.


Setup
=====

After bootstrapping::

    python bootstrap.py -v 1.7.0
    bin/buildout

Fire up both the uwsgi and the nginx servers in different consoles::

    bin/uwsgi --xml parts/uwsgi/uwsgi.xml
    bin/nginx-nodaemon


Problem description
===================

Works: "echo" module
--------------------
The subrequest method handling is valid when using the "echo" module::

    # testing subrequests against an "echo" location
    location /plain/echo/method {
        echo -n "request method was: ";
        echo $echo_request_method;
    }
    location /plain/echo/method/subrequest/echo {
        echo_subrequest POST /plain/echo/method;
    }

Proof::

    curl -X GET localhost:8088/plain/echo/method/subrequest/echo
    request method was: POST



Fails: "uwsgi" module
---------------------
The subrequest method handling fails when using the "uwsgi" module::

    # testing subrequests against an "uwsgi" location
    location /uwsgi/echo/method {
        include     ${openresty:location}/nginx/conf/uwsgi_params;
        uwsgi_pass  unix://${buildout:directory}/var/uwsgi/uwsgi.sock;
    }
    location /uwsgi/echo/method/subrequest/echo {
        echo_subrequest POST /uwsgi/echo/method;
    }

Proof::

    curl -X GET localhost:8088/uwsgi/echo/method/subrequest/echo
    request method was: GET


As we're doing an ``echo_subrequest POST ...`` like in
the example above, we would expect the same behavior here.


Appendix
========

FYI, this is the minimal uWSGI application mimicking ``echo $echo_request_method;``::

    def application(env, start_response):
        start_response('200 OK', [('Content-Type','text/plain')])
        response = 'request method was: {0}\n'.format(env['REQUEST_METHOD'])
        return response
