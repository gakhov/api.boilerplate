#!/usr/bin/env python
from setuptools import setup

exec(open("api/version.py").read())

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
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP"
    ],
    packages=["api"],
    install_requires=open("requirements.txt").readlines(),
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "start_server = api.start:start_server"
        ]
    }
)
