"""Validation schema for DELETE /document endpoint."""


OUTPUT_SCHEMA = {
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
    "additionalProperties": False,
    "required": ["id", "deleted_at"]
}
