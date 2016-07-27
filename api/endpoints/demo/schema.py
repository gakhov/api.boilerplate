
POST_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {
            "type": "string"
        }
    },
    "required": ["text"]
}

POST_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string"
        },
        "created_at": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": ["id"]
}

GET_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string"
        },
        "text": {
            "type": "string"
        },
        "created_at": {
            "type": "string",
            "format": "date-time"
        },
        "updated_at": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": ["id", "text", "created_at"]
}

PUT_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {
            "type": "string"
        }
    },
    "required": ["text"]
}

PUT_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string"
        },
        "updated_at": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": ["id"]
}

DELETE_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {
            "type": "string"
        },
        "deleted_at": {
            "type": "string",
            "format": "date-time"
        }
    },
    "required": ["id"]
}
