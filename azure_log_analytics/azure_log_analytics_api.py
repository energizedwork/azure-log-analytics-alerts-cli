from azure.mgmt.loganalytics.log_analytics_management_client import LogAnalyticsManagementClientConfiguration
from msrest import Deserializer
from msrest import Serializer
from msrest import ServiceClient
from msrest.exceptions import DeserializationError

from azure_log_analytics import models
from azure_log_analytics.operations.alert_services_operations import AlertServicesOperations


class LogAnalyticsAlertClient(object):

    def __init__(self, credentials, subscription_id, base_url=None):
        self.config = LogAnalyticsManagementClientConfiguration(credentials, subscription_id, base_url)
        self._client = ServiceClient(self.config.credentials, self.config)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}

        self._serialize = Serializer(client_models)
        self._serialize.serialize_type["dict"] = self._patched_serialize_dict

        self._deserialize = Deserializer(client_models)
        self._deserialize.basic_types[unicode] = "unicode"
        self._deserialize.deserialize_type["dict"] = self._patched_deserialize_dict
        self._deserialize.deserialize_type["list"] = self._patched_deserialize_iter

        self.alert_services = AlertServicesOperations(self._client, self.config, self._serialize, self._deserialize)

    def _patched_serialize_dict(self, attr, **kwargs):
        """Hack for MS Serialization class which can't handle Dictionaries properly
        """
        serialized = {}
        for key, value in attr.items():
            try:
                if isinstance(value, list):
                    serialized[self._serialize.serialize_unicode(key)] = self._serialize.serialize_iter(value, "str", **kwargs)
                else:
                    serialized[self._serialize.serialize_unicode(key)] = self._serialize.serialize_data(value, type(value).__name__, **kwargs)
            except ValueError:
                serialized[self._serialize.serialize_unicode(key)] = None
        return serialized

    def _patched_deserialize_dict(self, attr):
        if isinstance(attr, list):
            return {x['key']: self._deserialize.deserialize_data(x['value'], type(x["value"]).__name__) for x in attr}

        return {k: self._deserialize.deserialize_data(v, type(v).__name__) for k, v in attr.items()}

    def _patched_deserialize_iter(self, attr):
        if attr is None:
            return None

        if not isinstance(attr, (list, set)):
            raise DeserializationError("Cannot deserialize as [{}] an object of type {}".format(type(attr).__name__, type(attr)))

        return [self._deserialize.deserialize_data(a, type(a).__name__) for a in attr]


