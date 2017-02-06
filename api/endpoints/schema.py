# -*- coding: utf-8 -*-

__all__ = [
    "HEALTH_SCHEMA"
]

HEALTH_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "status": {
            "type": "string",
            "enum": [
                "ok",
                "warning",
                "error"
            ]
        },
        "checks": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": True,
                "properties": {
                    "name": {
                        "type": "string",
                        "minLength": 1
                    },
                    "status": {
                        "type": "string",
                        "enum": [
                            "ok",
                            "warning",
                            "error"
                        ]
                    },
                    "reason": {
                        "type": "string"
                    }
                },
                "required": [
                    "name",
                    "status"
                ]
            }
        }
    },
    "required": [
        "status",
        "checks"
    ]
}
