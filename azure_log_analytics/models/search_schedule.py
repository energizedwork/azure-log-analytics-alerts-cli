from msrest.serialization import Model


class SearchSchedule(Model):
    """Value object for saved search results.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: The id of the saved search.
    :vartype id: str
    :param etag: The etag of the saved search.
    :type etag: str
    :param category: The category of the saved search. This helps the user to
     find a saved search faster.
    :type category: str
    :param display_name: Saved search display name.
    :type display_name: str
    :param query: The query expression for the saved search. Please see
     https://docs.microsoft.com/en-us/azure/log-analytics/log-analytics-search-reference
     for reference.
    :type query: str
    :param version: The version number of the query lanuage. Only verion 1 is
     allowed here.
    :type version: long
    :param tags: The tags attached to the saved search.
    :type tags: list of :class:`Tag <azure.mgmt.loganalytics.models.Tag>`
    """

    _validation = {
        'id': {'readonly': True},
        'interval': {'required': True},
        'querytimespan': {'required': True},
        'active': {'required': True},
        'version': {'required': True, 'maximum': 1, 'minimum': 1},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'etag': {'key': 'etag', 'type': 'str'},
        'interval': {'key': 'properties.Interval', 'type': 'int'},
        'querytimespan': {'key': 'properties.QueryTimeSpan', 'type': 'int'},
        'active': {'key': 'properties.Active', 'type': 'str'},
        'version': {'key': 'properties.Version', 'type': 'long'},
        'tags': {'key': 'properties.Tags', 'type': '[Tag]'},
    }

    def __init__(self, interval, querytimespan, active, version=1, etag=None, tags=None):
        self.id = None
        self.etag = etag
        self.interval = interval
        self.querytimespan = querytimespan
        self.active = active
        self.version = version
        self.tags = tags
