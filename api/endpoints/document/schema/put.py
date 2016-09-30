"""Validation schema for PUT /document endpoint."""


INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {
            "type": "string"
        }
    },
    "additionalProperties": False
}

OUTPUT_SCHEMA = {
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
    "additionalProperties": False,
    "required": ["id", "updated_at"]
}
