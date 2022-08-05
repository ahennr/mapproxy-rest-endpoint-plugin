import logging

from mapproxy.script.util import register_command

from mapproxy_rest_endpoint.script.seeding_endpoint import service_seed_endpoint_command

plugin_logger = logging.getLogger('terrestris.rest.endpoint')

already_executed = False


def plugin_entrypoint():
    """ Entry point of the plugin, called by mapproxy """

    logging.info('Register WSGI REST endpoint')
    global already_executed
    if already_executed:
        return
    already_executed = True

    register_command('serve-seed-endpoint', {
        'func': service_seed_endpoint_command,
        'help': 'Service REST endpoint to handle seeding requests'
    })
    logging.info('…WSGI REST endpoint registered')
