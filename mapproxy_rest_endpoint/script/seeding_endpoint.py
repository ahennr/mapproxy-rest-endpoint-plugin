import logging
import optparse
import sys

from mapproxy.config.loader import ConfigurationError
from mapproxy.script.util import parse_bind_address
from werkzeug import run_simple

from mapproxy_rest_endpoint.app.wsgiseedapp import make_wsgi_seed_app


def service_seed_endpoint_command(args=None):
    parser = optparse.OptionParser("usage: %prog serve-seed-endpoint [options] projects/")
    parser.add_option("-b", "--bind",
                      dest="address", default='127.0.0.1:9090',
                      help="Server socket [127.0.0.1:9090]")
    parser.add_option("--debug", default=False, action='store_true',
                      dest="debug",
                      help="Enable debug mode")
    options, args = parser.parse_args(args)
    host, port = parse_bind_address(options.address)

    if len(args) != 2:
        parser.print_help()
        logging.error("ERROR: MapProxy configuration required.")
        sys.exit(1)
    mapproxy_conf = args[1]

    try:
        app = make_wsgi_seed_app(mapproxy_conf, debug=options.debug)
    except ConfigurationError:
        sys.exit(2)

    run_simple(host, port, app, use_reloader=True, processes=1,
               threaded=True, passthrough_errors=True)
