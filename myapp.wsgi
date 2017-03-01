#!/usr/bin/python

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/catalog")

# import *
# import application as app
# application.secret_key = 'Add your secret key'


def application(environ, start_response):
    status = '200 OK'
    output = 'hello world seems to be working'

    response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    # output = str(sys.path)

    return [output]

# import sys
# import logging
# logging.basicConfig(stream=sys.stderr)
# sys.path.insert(0,"/var/www/Catalog")

# from application import app as application
# application.secret_key = 'Add your secret key'


#WSGIServer(app).run()
