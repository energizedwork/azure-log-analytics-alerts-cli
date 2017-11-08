from msrest.serialization import Model


class ScheduleWebhook(Model):

    _validation = {
        'id': {'readonly': True},
        'name': {'required': True},
        'type': {'required': True},
        'webhook_uri': {'required': True},
        'custom_payload': {'required': False},
        'version': {'required': True, 'maximum': 1, 'minimum': 1},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'etag': {'key': 'etag', 'type': 'str'},
        'name': {'key': 'properties.Name', 'type': 'str'},
        'type': {'key': 'properties.Type', 'type': 'str'},
        'webhook_uri': {'key': 'properties.WebhookUri', 'type': 'str'},
        'custom_payload': {'key': 'properties.CustomPayload', 'type': 'str'},
        'version': {'key': 'properties.Version', 'type': 'long'},
        'tags': {'key': 'properties.Tags', 'type': '[Tag]'},
    }

    def __init__(self, name, webhook_uri, custom_payload, version=1, type="Webhook", etag=None, tags=None):
        self.id = None
        self.etag = etag
        self.name = name
        self.type = type
        self.webhook_uri = webhook_uri
        self.custom_payload = custom_payload
        self.version = version
        self.tags = tags
