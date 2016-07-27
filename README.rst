*********************
Tornado-based boilerplate for API projects
*********************

.. image:: https://travis-ci.org/gakhov/api.boilerplate.svg?branch=master
:target: https://travis-ci.org/gakhov/api.boilerplate


===========
How to run
===========

.. code-block:: bash

    $ bin/start_server -h
    usage: start_server [-h] [--name NAME] [--port PORT] [--settings SETTINGS]
    $ bin/start_server --name server --port 5570


=======================
Configuration
=======================

We support 3 different environments: `testing`, `staging` and `production`. The deployment settings for them are stored in `etc/deploy.json`.

-----------
Deployment
-----------

.. code-block:: bash

    $ make
    $ bin/buildout
    $ bin/fab staging deploy


---------------------
Server configuration
---------------------

.. code-block:: javascript

    {
        tbd.
    }


.. code-block:: bash

    $ bin/start_server --settings '{}'

