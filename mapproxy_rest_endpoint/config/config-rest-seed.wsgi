# WSGI module for use with Apache mod_wsgi or gunicorn

# # uncomment the following lines for logging
# # create a log.ini with `mapproxy-util create -t log-ini`
# from logging.config import fileConfig
# import os.path
# fileConfig(r'%(here)s/log.ini', {'here': os.path.dirname(__file__)})

# create wsgi app for mapproxy seed endpoint (default: port 9090)
from mapproxy_rest_endpoint.app.wsgiseedapp import make_wsgi_seed_app
application = make_wsgi_seed_app(r'%(mapproxy_conf)s')
