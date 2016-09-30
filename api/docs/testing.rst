Testing
========

External API Testing
---------------------

You can include a special query parameter `_test=true` to indicate that the requests you
are performing is a test requests.


.. warning::

    To use `_test=true` parameter the use has to have either `__all`, or `__test` access scope.


Build-In Tests
-------------------

.. warning::

    By default, the deployment script runs all test sets as a part of the deployment process.
    If not all of yours tests are passed, it will break the automated deployment process.


Unittest and functional tests
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To run unittests and functional tests:

::

   make test


Integration tests
^^^^^^^^^^^^^^^^^^^^^^^^

To run integration tests:

::

   make integration-test


All in One
^^^^^^^^^^^^^^^^

In case you need to run both test sets, just execute:

::

    make all-tests
