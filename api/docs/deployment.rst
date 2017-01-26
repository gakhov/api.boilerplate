How to Deploy
==============

There are 4 different deployment environments: ``local``, ``testing``, ``staging`` and ``production``.
Configuration parameters for each of them could be found in :file:`etc/deploy.json`.

The application checks the special environment variable ``API_ENV`` to recognize which
of the environments is active.

.. note::

    With the automated deployment via ``bin/fab`` the ``API_ENV`` environment variable is set
    automatically in a supervisor.

.. note::

    In all environments (except ``local``) logs are forwarded to ``syslog`` (``local2``) if
    ``IN_DOCKER_CONTAINER`` is `false`, otherwise - to standard output.


.. warning::

    By default, the deployment script runs all test sets as part of the deployment process.
    If not all of your tests are passed, they will break the automated deployment process.


++++++++++++++++++++++++++++++
Local environment
++++++++++++++++++++++++++++++

This is a special type of environment which doesn't require automated deployment and set as default.

For the `local` environment setup is a simple consequence of the following steps:

::

    make
    make develop

To start the `server` instance that will serve all supported endpoints.

::

    bin/start_server
    usage: start_server [-h] [--settings SETTINGS] [--name NAME] [--port PORT]


To start process with the specific `endpoint` only (from the list of registered endpoints):

::

    bin/start_endpoint search 5788
    usage: start_endpoint [-h] [--settings SETTINGS] name port


To generate the documentation:

::

    make docs


It will generate docs and make them available for browsing at :file:`documentation/html/index.html`


To generate the Swagger schema for the API:

::

    make swagger


It will generate schema and make it available for browsing at :file:`documentation/swagger/index.html`


++++++++++++++++++++++++++++++
Testing environment
++++++++++++++++++++++++++++++

API for `testing` environment (``API_ENV=testing``) could be deployed from any branch,
specified in :file:`etc/deploy.json` (e.g.  `master`)

::

    bin/fab testing deploy


.. note::

    Documentation and Swagger schema definitions will be generated as a part
    of the deployment process.


++++++++++++++++++++++++++++++
Staging environment
++++++++++++++++++++++++++++++

API for `staging` environment (``API_ENV=staging``) could be deployed from any branch,
specified in :file:`etc/deploy.json` (e.g.  `master`)

::

    bin/fab staging deploy


.. note::

    Documentation and Swagger schema definitions will be generated as a part
    of the deployment process.

++++++++++++++++++++++++++++++
Production environment
++++++++++++++++++++++++++++++

API for `production` environment (``API_ENV=production``) could be deployed from tags ONLY, specified in :file:`etc/deploy.json` (e.g.  `0.1.0`)

::

    bin/fab production deploy


.. warning::

    It's not recommended to make any changes or run additional processes without changing :file:`etc/production/supervisord.conf.template` and re-deploying the application.


.. note::

    Documentation and Swagger schema definitions will be generated as a part
    of the deployment process.
