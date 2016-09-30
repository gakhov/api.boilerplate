#!/usr/bin/env python
from setuptools import setup

execfile('api/version.py')

setup(
    name="api.boilerplate",
    version=__version__,
    author="Andrii Gakhov",
    author_email="andrii.gakhov@gmail.com",
    description="Tornado-based boilerplate for API projects",
    long_description=open("README.rst").read(),
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP"
    ],
    packages=["api"],
    include_package_data=True,
    extras_require=dict(
        test=[
            "pytest>=3.0.1,<4.0.0",
            "pytest-cov==2.3.0",
            "pytest-pep8==1.0.6",
            "mock==2.0.0",
            "sphinx==1.4.5",
            "fabric==1.12.0",
        ],
    ),
    install_requires=[
        "futures>=3.0,<3.1",
        "jsonschema==2.5.1",
        "redis>=2.10,<2.11",
        "requests[security]>=2.10,<3.0",
        "strict_rfc3339==0.5",  # for jsonschema to validate date-time
        "tornado>=4.0,<5.0",
    ],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "start_server = api.start:start_server",
            "start_endpoint = api.start:start_endpoint",
        ]
    }
)
