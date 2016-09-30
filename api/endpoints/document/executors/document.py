from datetime import datetime

from ....exceptions import APIClientError


class DocumentEndpointExecutor(object):
    """Document endpoint executor."""

    def __init__(self, user_id, test=None):
        self._user_id = user_id
        self._test = test is True

    def _get_or_raise(self, document_id):
        """Get a document or raise APIClientError."""
        try:
            document = {
                "id": "lu165gsQI9cxly2J3MM",
                "text": (
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                    "sed do eiusmod tempor incididunt ut labore et dolore "
                    "magna aliqua."
                ),
                "created_at": "2007-07-07T13:30:00Z"
            }
        except:
            raise APIClientError(404, "Document not found",
                                 "Document {} not found".format(document_id))
        return document

    def get(self, document_id):
        document = self._get_or_raise(document_id)
        return document

    def create(self, params):
        result = {
            "id": "lu165gsQI9cxly2J3MM",
            "created_at": "2016-07-07T13:30:00Z"
        }
        return result

    def update(self, document_id, params):
        result = {
            "id": document_id,
            "updated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        return result

    def delete(self, document_id):
        result = {
            "id": document_id,
            "deleted_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        return result
