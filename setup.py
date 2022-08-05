from setuptools import setup, find_packages

install_requires = [
    'mapproxy>=1.15'
]

readme = open('README.md', encoding="utf-8").read()

setup(
    name="mapproxy-rest-endpoint",
    python_requires='>=3.7',
    version="0.0.1",
    description="Plugin for MapProxy adding REST Seeding enpoint",
    long_description=readme,
    long_description_content_type='text/x-rst',
    author="André Henn",
    author_email="henn@terrestris.de",
    url="https://github.com/ahennr/mapproxy-rest-endpoint",
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.yaml']},
    install_requires=install_requires,

    # the following makes a plugin available to mapproxy
    entry_points={"mapproxy": ["rest_endpoint = mapproxy_rest_endpoint.pluginmodule"]},

    # custom PyPI classifier for mapproxy plugins
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    zip_safe=False
)
