import uuid

from msrest.pipeline import ClientRawResponse
from msrestazure.azure_exceptions import CloudError


class AlertServicesOperations(object):
    def __init__(self, client, config, serializer, deserializer):

        self._client = client
        self._serialize = serializer
        self._deserialize = deserializer
        self.api_version = "2015-03-20"

        self.config = config

    def delete_search_schedule(self, resource_group_name, workspace_name, saved_search_name, schedule_name, parameters=None, custom_headers=None, raw=False, **operation_config):
        """Deletes the specified saved search in a given workspace.

        :param resource_group_name: The name of the resource group to get. The
         name is case insensitive.
        :type resource_group_name: str
        :param workspace_name: Log Analytics workspace name
        :type workspace_name: str
        :param saved_search_name: Name of the saved search.
        :type saved_search_name: str
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: None or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>` if
         raw=true
        :rtype: None or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
        :raises: :class:`CloudError<msrestazure.azure_exceptions.CloudError>`
        """
        # Construct URL
        url = '/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationalInsights/workspaces/{workspaceName}/savedSearches/{savedSearchName}/schedules/{scheduleName}'
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1, pattern=r'^[-\w\._\(\)]+$'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'savedSearchName': self._serialize.url("saved_search_name", saved_search_name, 'str'),
            'scheduleName': self._serialize.url("schedule_name", schedule_name, 'str'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        model_name = 'SearchSchedule'
        body_content, header_parameters, query_parameters = self._prepare_request(custom_headers, parameters, model_name)

        request = self._client.delete(url, query_parameters)
        response = self._client.send(request, header_parameters, **operation_config)

        return self._handle_response(response, raw, model_name)

    def delete_schedule_threshold(self, resource_group_name, workspace_name, saved_search_name, schedule_name, action_name, parameters=None, custom_headers=None, raw=False, **operation_config):
        # Construct URL
        url = '/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationalInsights/workspaces/{workspaceName}/savedSearches/{savedSearchName}/schedules/{scheduleName}/actions/{actionName}'
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1, pattern=r'^[-\w\._\(\)]+$'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'savedSearchName': self._serialize.url("saved_search_name", saved_search_name, 'str'),
            'scheduleName': self._serialize.url("schedule_name", schedule_name, 'str'),
            'actionName': self._serialize.url("action_name", action_name, 'str'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')
        }
        url = self._client.format_url(url, **path_format_arguments)

        model_name = 'ScheduleThreshold'
        body_content, header_parameters, query_parameters = self._prepare_request(custom_headers, parameters, model_name)

        request = self._client.delete(url, query_parameters)
        response = self._client.send(request, header_parameters, **operation_config)

        return self._handle_response(response, raw, model_name)

    def create_schedule(self, resource_group_name, workspace_name, saved_search_name, schedule_name, parameters, custom_headers=None, raw=False, **operation_config):
        """Creates or updates a saved search for a given workspace.

        :param resource_group_name: The name of the resource group to get. The
         name is case insensitive.
        :type resource_group_name: str
        :param workspace_name: Log Analytics workspace name
        :type workspace_name: str
        :param saved_search_name: The id of the saved search.
        :type saved_search_name: str
        :param parameters: The parameters required to save a search.
        :type parameters: :class:`SavedSearch
         <azure.mgmt.loganalytics.models.SavedSearch>`
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: :class:`SavedSearch
         <azure.mgmt.loganalytics.models.SavedSearch>` or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>` if
         raw=true
        :rtype: :class:`SavedSearch
         <azure.mgmt.loganalytics.models.SavedSearch>` or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
        :raises: :class:`CloudError<msrestazure.azure_exceptions.CloudError>`
        """
        # Construct URL
        url = '/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationalInsights/workspaces/{workspaceName}/savedSearches/{savedSearchName}/schedules/{scheduleName}'
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1, pattern=r'^[-\w\._\(\)]+$'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'savedSearchName': self._serialize.url("saved_search_name", saved_search_name, 'str'),
            'scheduleName': self._serialize.url("schedule_name", schedule_name, 'str'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')}
        url = self._client.format_url(url, **path_format_arguments)

        model_name = 'SearchSchedule'
        body_content, header_parameters, query_parameters = self._prepare_request(custom_headers, parameters, model_name)

        request = self._client.put(url, query_parameters)
        response = self._client.send(request, header_parameters, body_content, **operation_config)

        return self._handle_response(response, raw, model_name)

    def create_webhook(self, resource_group_name, workspace_name, saved_search_name, schedule_name, action_name, parameters, custom_headers=None, raw=False, **operation_config):
        """Creates or updates a saved search for a given workspace.

        :param resource_group_name: The name of the resource group to get. The
         name is case insensitive.
        :type resource_group_name: str
        :param workspace_name: Log Analytics workspace name
        :type workspace_name: str
        :param saved_search_name: The id of the saved search.
        :type saved_search_name: str
        :param parameters: The parameters required to save a search.
        :type parameters: :class:`SavedSearch
         <azure.mgmt.loganalytics.models.SavedSearch>`
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: :class:`SavedSearch
         <azure.mgmt.loganalytics.models.SavedSearch>` or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>` if
         raw=true
        :rtype: :class:`SavedSearch
         <azure.mgmt.loganalytics.models.SavedSearch>` or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
        :raises: :class:`CloudError<msrestazure.azure_exceptions.CloudError>`
        """
        # Construct URL
        url = '/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationalInsights/workspaces/{workspaceName}/savedSearches/{savedSearchName}/schedules/{scheduleName}/actions/{actionName}'
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1, pattern=r'^[-\w\._\(\)]+$'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'savedSearchName': self._serialize.url("saved_search_name", saved_search_name, 'str'),
            'scheduleName': self._serialize.url("schedule_name", schedule_name, 'str'),
            'actionName': self._serialize.url("name", action_name, 'str'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')}
        url = self._client.format_url(url, **path_format_arguments)

        model_name = 'ScheduleWebhook'
        body_content, header_parameters, query_parameters = self._prepare_request(custom_headers, parameters, model_name)

        request = self._client.put(url, query_parameters)
        response = self._client.send(request, header_parameters, body_content, **operation_config)

        return self._handle_response(response, raw, model_name)

    def create_threshold(self, resource_group_name, workspace_name, saved_search_name, schedule_name, action_name, parameters, custom_headers=None, raw=False, **operation_config):
        """Creates or updates a saved search for a given workspace.

        :param resource_group_name: The model_name of the resource group to get. The
         model_name is case insensitive.
        :type resource_group_name: str
        :param workspace_name: Log Analytics workspace model_name
        :type workspace_name: str
        :param saved_search_name: The id of the saved search.
        :type saved_search_name: str
        :param parameters: The parameters required to save a search.
        :type parameters: :class:`SavedSearch
         <azure.mgmt.loganalytics.models.SavedSearch>`
        :param dict custom_headers: headers that will be added to the request
        :param bool raw: returns the direct response alongside the
         deserialized response
        :param operation_config: :ref:`Operation configuration
         overrides<msrest:optionsforoperations>`.
        :return: :class:`SavedSearch
         <azure.mgmt.loganalytics.models.SavedSearch>` or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>` if
         raw=true
        :rtype: :class:`SavedSearch
         <azure.mgmt.loganalytics.models.SavedSearch>` or
         :class:`ClientRawResponse<msrest.pipeline.ClientRawResponse>`
        :raises: :class:`CloudError<msrestazure.azure_exceptions.CloudError>`
        """
        # Construct URL
        url = '/subscriptions/{subscriptionId}/resourcegroups/{resourceGroupName}/providers/Microsoft.OperationalInsights/workspaces/{workspaceName}/savedSearches/{savedSearchName}/schedules/{scheduleName}/actions/{actionName}'
        path_format_arguments = {
            'resourceGroupName': self._serialize.url("resource_group_name", resource_group_name, 'str', max_length=90, min_length=1, pattern=r'^[-\w\._\(\)]+$'),
            'workspaceName': self._serialize.url("workspace_name", workspace_name, 'str'),
            'savedSearchName': self._serialize.url("saved_search_name", saved_search_name, 'str'),
            'scheduleName': self._serialize.url("schedule_name", schedule_name, 'str'),
            'actionName': self._serialize.url("name", action_name, 'str'),
            'subscriptionId': self._serialize.url("self.config.subscription_id", self.config.subscription_id, 'str')}
        url = self._client.format_url(url, **path_format_arguments)

        model_name = 'ScheduleThreshold'
        body_content, header_parameters, query_parameters = self._prepare_request(custom_headers, parameters, model_name)

        request = self._client.put(url, query_parameters)
        response = self._client.send(request, header_parameters, body_content, **operation_config)

        return self._handle_response(response, raw, model_name)

    def _handle_response(self, response, raw, model_name):
        if response.status_code == 409:
            #"Error '409 Conflict'. The resource already exists. Resource updates not supported."
            return

        if response.status_code == 404:
            #"Error '404 Not Found'. The resource doesn't exists."
            return

        if response.status_code not in [200, 202]:
            exp = CloudError(response)
            exp.request_id = response.headers.get('x-ms-request-id')
            raise exp

        if response.status_code == 200:
            deserialized = self._deserialize(model_name, response)

            if raw:
                client_raw_response = ClientRawResponse(deserialized, response)
                return client_raw_response

            return deserialized

    def _prepare_request(self, custom_headers, parameters, model_name):
        query_parameters = {'api-version': self._serialize.query("self.api_version", self.api_version, 'str')}
        header_parameters = {'Content-Type': 'application/json; charset=utf-8'}

        if self.config.generate_client_request_id:
            header_parameters['x-ms-client-request-id'] = str(uuid.uuid1())
        if custom_headers:
            header_parameters.update(custom_headers)
        if self.config.accept_language is not None:
            header_parameters['accept-language'] = self._serialize.header("self.config.accept_language", self.config.accept_language, 'str')

        if parameters:
            body_content = self._serialize.body(parameters, model_name)
        else:
            body_content = None

        return body_content, header_parameters, query_parameters




#def delete_schedule_alert(self, search_name, schedule_name, action_name):
 #   return self._validate_response(requests.delete(self.base_url + "savedSearches/{}/schedules/{}/actions/{}".format(search_name, schedule_name, action_name), params=self.PARAMS, headers=self.HEADERS))

# def create_schedule_alert_threshold(self, search_name, alert_name, threshold_operator, threshold_value, severity="Critical", include_email_alert=True, email_recipients=list(), email_subject=None):
#     properties = {
#         "name": alert_name,
#         "severity": severity, #Critial, Warning, Informational
#         "Type": "Alert",
#         "threshold": {
#             "operator": threshold_operator,
#             "value": threshold_value
#         },
#         "version": 1
#     }
#
#     if include_email_alert:
#         properties["emailnotification"] = {
#             "recipients": email_recipients,
#             "subject": email_subject
#         }
#
#     data = {
#         "properties": properties
#     }
#
#     return self._validate_response(requests.put(self.base_url + "savedSearches/{0}/schedules/{0}-schedule/actions/{0}-schedule-action-threshold".format(string.lower(search_name)), params=self.PARAMS, headers=self.HEADERS, data=json.dumps(data)))
#
