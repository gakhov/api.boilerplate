=========
Settings
=========

-------------------------
Configiration parameters
-------------------------


There are not so many configuration parameters and all of them could be found in :mod:api.settings.

+-----------------------------+-----------------------------------------------------------------------+
| ``default_server_name``     | default name for the server application while running on localhost    |
+-----------------------------+-----------------------------------------------------------------------+
| ``default_server_port``     | default port for the server application while running on localhost    |
+-----------------------------+-----------------------------------------------------------------------+
| ``registered_endpoints``    | list of registered endpoints (e.g. ``[demo, ]``)                      |
+-----------------------------+-----------------------------------------------------------------------+
| ``api_version``             | current version of the API as string (e.g. ``"1"``)                   |
+-----------------------------+-----------------------------------------------------------------------+
| ``deprecated_api_versions`` | list of deprecated versions (e.g. ``["0", ]``). If you specify        |
|                             | not empty list here, appliaction automatically create the appropriate |
|                             | URL with a special :class:`api.handlers.DeprecatedHandler`      |
|                             | that will return ``410 Gone`` HTTP Error.                             |
+-----------------------------+-----------------------------------------------------------------------+


------------------------
Environment variables
------------------------

+-------------------------------+-----------------------------------------------------------------------+
| ``API_ENV``                   | environment under which the application should be executed            |
+-------------------------------+-----------------------------------------------------------------------+


----------
Logging
----------

In `testing`, `staging`, `production` environments all output is routed to the syslog's `local2` that
could be configured to store it in a file, e.g. `/var/log/api.log`, using syslog.


.. automodule:: api.endpoints
   :members:
