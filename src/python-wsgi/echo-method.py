def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/plain')])
    response = 'request method was: {0}\n'.format(env['REQUEST_METHOD'])
    return response
