def get_schema():
    return {
        'type': 'object',
        'properties': {
            'connections': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'name': {'type': 'string'},
                        'path': {'type': 'string'},
                        'driver': {'type': 'string'},
                        'server': {'type': 'string'},
                        'database': {'type': 'string'},
                        'name_col': {'type': 'string'},
                        'text_col': {'type': 'string'},
                    }
                }
            },
            'documents': {'type': 'array', 'items': {'$ref': '#/definitions/document'}},
            'irr_documents': {'type': 'array', 'items': {'$ref': '#/definitions/document'}},
            'labels': {'type': 'array', 'items': {'type': 'string'}},
            'highlights': {'type': 'array', 'items': {'type': 'string'}},
            'project': {'type': 'string'},
            'start_date': {'type': 'string'},
            'end_date': {'type': 'string'},
            'annotation': {
                'type': 'object',
                'properties': {
                    'irr_percent': {'type': 'number'},
                    'irr_count': {'type': 'integer'},
                    'annotators': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'name': {'type': 'string'},
                                'number': {'type': 'integer'},
                                'percent': {'type': 'number', 'maximum': 1.0, 'minimum': 0.0},
                                'documents': {'type': 'array', 'items': {'$ref': '#/definitions/document'}},
                            },
                        },
                    },
                },
            }
        },
        'definitions': {
            'document': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'metadata': {'type': 'object'},
                    'text': {'type': 'string'},
                    'offsets': {'type': 'array', 'items': {'$ref': '#/definitions/offset'}},
                    'highlights': {'type': 'array', 'items': {'type': 'string'}},
                    'expiration_date': {'type': 'string'},
                }
            },
            'offset': {
                'type': 'object',
                'properties': {
                    'start': {'type': 'integer', 'minimum': 0},
                    'end': {'type': 'integer', 'minimum': 0}
                }
            },
        }
    }