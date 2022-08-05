# Mapproxy REST Seed / cleanup endpoint plugin

`mapproxy-rest-endpoint` is a plugin for [Mapproxy (version >= 1.15)](https://mapproxy.org/) which adds a command `serve-seed-endpoint` to `mapproxy-util`.
The `wsgi` file in `mapproxy_rest_endpoint/config/` contains a template for a corresponding application.

## Usage / Installation
### Docker (recommended)
Since this plugin provides a standalone application which runs *aside* a running mapproxy instance a more specific uwsgi configuration has to be defined:

```
[uwsgi]
master = true
chdir = /mapproxy
pyargv = /mapproxy.yaml
processes = 2
threads = 10
chmod-socket = 777
pidfile = /tmp/mapproxy-seed.pid
socket = 0.0.0.0:9090
wsgi-file = rest-seed.py
```
It's assumed that `rest-seed.py` contains the content of the abovementioned template, e.g:

```python
from mapproxy_rest_endpoint.app.wsgiseedapp import make_wsgi_seed_app

mapproxy_cfg_path = r'/mapproxy/mapproxy.yaml'

# create wsgi app for mapproxy seed endpoint (default: port 9090)
application = make_wsgi_seed_app(mapproxy_cfg_path)
```

The resulting docker configuration can be found [here](https://github.com/ahennr/docker-mapproxy/tree/seed-rest-endpoint-plugin).

The content in `mapproxy/` folder should look like this:

```
mapproxy/
⌊ mapproxy.yml
⌊ app.py # containing mapproxy app
⌊ rest-seed.py # containing rest seed endpoint
```

### Python - virtualenv:

```shell
python3 -m venv testenv
source testenv/bin/activate
pip install pip install pyproj six werkzeug uwsgi 'MapProxy>1.15'
pip install ./
```

Startup mapproxy using previously created virtualenv.

## Examples
#### Seed and cleanup via `REST` for list of levels:

See scratches in `examples/`