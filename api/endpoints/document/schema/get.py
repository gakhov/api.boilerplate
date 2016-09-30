"""Validation schema for GET /document endpoint."""


INPUT_SCHEMA = {
    "type": "object",
    "properties": {
    }
}

OUTPUT_SCHEMA = {
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
    "additionalProperties": False,
    "required": ["id", "text", "created_at"]
}
