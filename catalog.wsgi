#!/usr/bin/python
# import sys
# import logging
# logging.basicConfig(stream=sys.stderr)
# sys.path.insert(0,"/var/www/catalog")

# from project import app as application
# application.secret_key = 'Add your secret key'



def application(environ, start_response):
    status = '200 OK'
    output = 'hello world'

    response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
