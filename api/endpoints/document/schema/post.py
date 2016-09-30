"""Validation schema for POST /document endpoint."""


INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {
            "type": "string"
        }
    },
    "required": ["text"],
    "additionalProperties": False
}

OUTPUT_SCHEMA = {
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
    "additionalProperties": False,
    "required": ["id", "created_at"]
}
