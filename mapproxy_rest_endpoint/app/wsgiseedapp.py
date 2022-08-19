"""
The seeder WSGI application.
"""
from __future__ import print_function

import json
import logging
import re

from mapproxy.config.loader import load_configuration, ConfigurationError
from mapproxy.response import Response, status_code
from mapproxy.seed.cleanup import cleanup
from mapproxy.wsgiapp import wrap_wsgi_debug

from mapproxy.seed.cachelock import DummyCacheLocker
from mapproxy.seed.config import SeedingConfiguration, SeedConfigurationError
from mapproxy.seed.script import seed
from mapproxy.seed.util import ProgressLog

log = logging.getLogger('mapproxy_rest_endpoint')
log_wsgi_app = logging.getLogger('mapproxy.wsgiapp')


def make_wsgi_seed_app(services_conf=None, debug=False, ignore_warnings=False):
    """
    Create a Seed REST endpoint app
    """

    try:
        conf = load_configuration(mapproxy_conf=services_conf, ignore_warnings=ignore_warnings)
    except ConfigurationError as e:
        log.fatal(e)
        raise

    app = SeedRestApp(conf)
    if debug:
        app = wrap_wsgi_debug(app, {})

    return app


def not_supported_response():
    import mapproxy.version
    html = "<html><body><h1>Welcome to MapProxy Seed REST endpoint<br>HTTP - POST only<br>Version %s</h1>" \
           "</body></html>" % \
           mapproxy.version.version
    return Response(html, mimetype='text/html')


def result_resp(seed_tasks, cleanup_tasks):
    res = json.dumps({
        'successful': 'true',
        'seeds': list(map(lambda t: {'seed_name': t.md['name'],
                                     'cache_name': t.md['cache_name'],
                                     'grid_name': t.md['grid_name'],
                                     'timestamp': t.refresh_timestamp
                                     }, seed_tasks)),
        'cleanups': list(map(lambda t: {'cleanup_name': t.md['name'],
                                        'cache_name': t.md['cache_name'],
                                        'grid_name': t.md['grid_name'],
                                        'timestamp': t.remove_timestamp
                                        }, cleanup_tasks)),
    })
    return Response(res, mimetype='application/json')


def result_resp_error(seed_configuration_error=None):
    result = json.dumps({
        'successful': 'false',
        'seedConfigurationError': seed_configuration_error.args
    })
    return Response(result, mimetype='application/json', status=status_code(500))


class SeedRestApp(object):
    """
    The seed REST WSGI application.
    """
    handler_path_re = re.compile(r'^/(\w+)')

    def __init__(self, mapproxy_conf):
        self.mapproxy_conf = mapproxy_conf

    def __call__(self, environ, start_response):
        if environ['REQUEST_METHOD'] != 'POST':
            resp = not_supported_response()
            log.error('Request method not supported for seeding endpoint')
            return resp(environ, start_response)

        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            request_body_size = -1

        br = environ.get('wsgi.input')
        passed_config = json.loads(br.read(request_body_size))

        if "seedConfig" not in passed_config:
            return result_resp_error()(environ, start_response)

        seed_conf = passed_config['seedConfig']
        options = passed_config['config']

        seed_cfg = SeedingConfiguration(seed_conf, self.mapproxy_conf)
        try:
            seed_tasks = seed_cfg.seeds()
            cleanup_tasks = seed_cfg.cleanups()
        except SeedConfigurationError as sce:
            return result_resp_error(sce)(environ, start_response)

        # TODO: check if seeding can be performed in an asynchronous way -> Polling / Job queue / status
        cache_locker = DummyCacheLocker()
        logger = ProgressLog(verbose=True, silent=False)

        if seed_tasks:
            seed(seed_tasks, progress_logger=logger, dry_run=options['dry_run'],
                 concurrency=options['concurrency'], cache_locker=cache_locker,
                 skip_geoms_for_last_levels=options['geom_levels'])

        if cleanup_tasks:
            cleanup(cleanup_tasks, progress_logger=logger, dry_run=options['dry_run'],
                    concurrency=options['concurrency'],
                    skip_geoms_for_last_levels=options['geom_levels'])

        # return result
        resp = result_resp(seed_tasks, cleanup_tasks)
        return resp(environ, start_response)
