from msrest.serialization import Model


class ScheduleThreshold(Model):

    _validation = {
        'id': {'readonly': True},
        'name': {'required': True},
        'severity': {'required': True},
        'type': {'required': True},
        'threshold': {'required': True},
        'email_notification': {'required': False},
        'version': {'required': True, 'maximum': 1, 'minimum': 1},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'etag': {'key': 'etag', 'type': 'str'},
        'name': {'key': 'properties.Name', 'type': 'str'},
        'severity': {'key': 'properties.Severity', 'type': 'str'},
        'type': {'key': 'properties.Type', 'type': 'str'},
        'threshold': {'key': 'properties.Threshold', 'type': 'dict'},
        'email_notification': {'key': 'properties.EmailNotification', 'type': 'dict'},
        'version': {'key': 'properties.Version', 'type': 'long'},
        'tags': {'key': 'properties.Tags', 'type': '[Tag]'},
    }

    def __init__(self, name, severity, threshold, email_notification, version=1, type="Alert", etag=None, tags=None):
        self.id = None
        self.etag = etag
        self.name = name
        self.severity = severity
        self.type = type
        self.threshold = threshold
        self.email_notification = email_notification
        self.version = version
        self.tags = tags
