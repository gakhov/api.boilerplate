Versioning
===========

API clients can get all versions at once using a special top-level endpoint `_version`
that doesn't require any access_token.

^^^^^^^^
Request
^^^^^^^^

::

    curl -XGET -H "Content-type: application/json" "https://{SERVER}/_version"


^^^^^^^^
Response
^^^^^^^^

::

    {
        "build": "1.2.3",
        "version": "v1",
        "endpoints": {
            "document": "1.0.1"
        }
    }


Additionally, we include such versions in response headers: `X-Api-Version`,
 `X-Api-Build` and `X-Endpoint-Version`.


API Versioning
~~~~~~~~~~~~~~~

The API version is a current generation of the API. You shouldn't change
it quite often, keep it for cases when you completely change ideology
of the API or migrated to another platform. Such changes always not backward
compatible.

If you change the current API version (by editing `version.py`), consider
to include previous versions in the `deprecated_api_versions` parameter
of the settings.


Endpoint Versioning
~~~~~~~~~~~~~~~~~~~~

When clients rely on your endpoints you need a way to tell them that
particular endpoint has been changed and tell how big the changes were.
This could be done with Endpoint versioning (see property `version` of
each endpoint we have) and Semantic Versioning (see http://semver.org/)


Build Versioning
~~~~~~~~~~~~~~~~~

The Build Version is an indicator of the current release of your API,
which is not necessary contain any changes in endpoints or creates
a new API generation. Update such version as soon as you make a production release.

Usually, build version information is useful for debug and troubleshooting.
