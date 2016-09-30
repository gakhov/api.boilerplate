==================
/document endpoint
==================

---------------------
Retrieve a document
---------------------

^^^^^^^
Scopes
^^^^^^^

`get-document`, `update-document`


^^^^^^^^
Request
^^^^^^^^

::

    curl -XGET -H "Content-type: application/json" "https://{SERVER}/v1/document/lu165gsQI9cxly2J3MM?access_token={TOKEN}"


^^^^^^^^
Response
^^^^^^^^

::

    {
        "id": "lu165gsQI9cxly2J3MM",
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "created_at": "2007-07-07T13:30:00Z"
    }


----------------------
Create a new document
----------------------

^^^^^^^
Scopes
^^^^^^^

`create-document`


^^^^^^^^
Request
^^^^^^^^

::

    curl -XPOST -H "Content-type: application/json" "https://{SERVER}/v1/document?access_token={TOKEN}" -d '{
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    }'


^^^^^^^^
Response
^^^^^^^^

::

    {
        "id": "lu165gsQI9cxly2J3MM",
        "created_at": "2016-07-07T13:30:00Z"
    }


------------------
Update a document
------------------

^^^^^^^
Scopes
^^^^^^^

`update-document`



^^^^^^^^
Request
^^^^^^^^

::

    curl -XPUT -H "Content-type: application/json" "https://{SERVER}/v1/document/lu165gsQI9cxly2J3MM?access_token={TOKEN}" -d '{
        "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    }'


^^^^^^^^
Response
^^^^^^^^

::

    {
        "id": "lu165gsQI9cxly2J3MM",
        "updated_at": "2016-07-27T13:30:00Z"
    }


------------------
Delete a document
------------------

^^^^^^^
Scopes
^^^^^^^

`delete-document`



^^^^^^^^
Request
^^^^^^^^

::

    curl -XDELETE -H "Content-type: application/json" "https://{SERVER}/v1/document/lu165gsQI9cxly2J3MM?access_token={TOKEN}"


^^^^^^^^
Response
^^^^^^^^

::

    {
        "id": "lu165gsQI9cxly2J3MM",
        "deleted_at": "2016-08-11T12:04:58Z"
    }
