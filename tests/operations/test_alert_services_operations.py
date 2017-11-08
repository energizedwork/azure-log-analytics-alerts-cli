import os
import unittest

from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.mgmt.loganalytics.models import SavedSearch
from msrestazure.azure_active_directory import ServicePrincipalCredentials
from azure_log_analytics.azure_log_analytics_api import LogAnalyticsAlertClient
from azure_log_analytics.models import ScheduleThreshold
from azure_log_analytics.models import ScheduleWebhook
from azure_log_analytics.models import SearchSchedule


class TestAlertServicesOperations(unittest.TestCase):

    RESOURCE_GROUP = "defaultresourcegroup-suk"
    WORKSPACE_NAME = "defaultworkspace-1e6df27b-3c77-431f-a405-cc7233ee89d5-suk"
    CATEGORY = "integration-tests"
    SAVED_SEARCH_NAME = "test-search"
    SCHEDULE_NAME = "test-search-schedule"
    THRESHOLD_ACTION_NAME = "test-search-schedule-threshold"
    WEBHOOK_ACTION_NAME = "test-search-schedule-webhook"
    SAMPLE_QUERY = "Type=Perf ObjectName=\"Processor\" CounterName=\"% Processor Time\" Computer=\"ACUKSLDSTANAP01\" | measure avg(CounterValue) by Computer Interval 5MINUTES"

    def setUp(self):
        tenant_id = os.environ.get("TF_VAR_azure_tenant_id")
        client_id = os.environ.get("TF_VAR_azure_client_id")
        client_secret = os.environ.get("TF_VAR_azure_client_secret")
        subscription_id = os.environ.get("TF_VAR_azure_subscription_id")

        if not tenant_id or not client_id or not client_secret or not subscription_id:
            raise ValueError("one or more environment variables are missing")

        credentials = ServicePrincipalCredentials(client_id, client_secret, tenant=tenant_id, verify=True, resource="https://management.azure.com/")
        self.laa_client = LogAnalyticsAlertClient(credentials, subscription_id)
        self.lam_client = LogAnalyticsManagementClient(credentials, subscription_id)

        self.clean_up()

    def tearDown(self):
        self.clean_up()

    def clean_up(self):
        """This is called at setup and teardown as there is sometimes a delay for Azure finish deletes.
           This can result in 409 Conflict error messages during a test run
        """
        try:
            self.lam_client.saved_searches.delete(self.RESOURCE_GROUP, self.WORKSPACE_NAME, self.SAVED_SEARCH_NAME)
        except AttributeError as e:
            if e.args[0] == "'NoneType' object has no attribute 'error'":  # Azure lib doesn't deserialize error non-200 responses properly
                pass

        self.laa_client.alert_services.delete_search_schedule(self.RESOURCE_GROUP, self.WORKSPACE_NAME, self.SAVED_SEARCH_NAME, self.SCHEDULE_NAME)
        self.laa_client.alert_services.delete_schedule_threshold(self.RESOURCE_GROUP, self.WORKSPACE_NAME, self.SAVED_SEARCH_NAME, self.SCHEDULE_NAME, self.THRESHOLD_ACTION_NAME)
        self.laa_client.alert_services.delete_schedule_threshold(self.RESOURCE_GROUP, self.WORKSPACE_NAME, self.SAVED_SEARCH_NAME, self.SCHEDULE_NAME, self.WEBHOOK_ACTION_NAME)

    def test_can_create_saved_search(self):

        result = self.lam_client.saved_searches.create_or_update(
            self.RESOURCE_GROUP,
            self.WORKSPACE_NAME,
            self.SAVED_SEARCH_NAME,
            SavedSearch(self.CATEGORY, self.SAVED_SEARCH_NAME, self.SAMPLE_QUERY, 1)
        )

        self.assertTrue(isinstance(result, SavedSearch))
        self.assertTrue(result.id)
        self.assertEqual(result.display_name, self.SAVED_SEARCH_NAME)

    def test_can_create_schedule(self):

        result = self.lam_client.saved_searches.create_or_update(
            self.RESOURCE_GROUP,
            self.WORKSPACE_NAME,
            self.SAVED_SEARCH_NAME,
            SavedSearch(self.CATEGORY, self.SAVED_SEARCH_NAME, self.SAMPLE_QUERY, 1)
        )

        self.assertTrue(isinstance(result, SavedSearch))

        result = self.laa_client.alert_services.create_schedule(
            self.RESOURCE_GROUP,
            self.WORKSPACE_NAME,
            self.SAVED_SEARCH_NAME,
            self.SCHEDULE_NAME,
            SearchSchedule(5, 5, True)
        )

        self.assertTrue(isinstance(result, SearchSchedule))

    def test_can_create_threshold(self):
        self.lam_client.saved_searches.create_or_update(
            self.RESOURCE_GROUP,
            self.WORKSPACE_NAME,
            self.SAVED_SEARCH_NAME,
            SavedSearch(self.CATEGORY, self.SAVED_SEARCH_NAME, self.SAMPLE_QUERY, 1)
        )

        self.laa_client.alert_services.create_schedule(
            self.RESOURCE_GROUP,
            self.WORKSPACE_NAME,
            self.SAVED_SEARCH_NAME,
            self.SCHEDULE_NAME,
            SearchSchedule(5, 5, True)
        )

        parameters = ScheduleThreshold(self.THRESHOLD_ACTION_NAME, "Critical", {"operator": "gt", "value": "80"}, {"recipients": ["bob@kelso.co.ed"], "subject": "Test Alert"})

        result = self.laa_client.alert_services.create_threshold(
            self.RESOURCE_GROUP,
            self.WORKSPACE_NAME,
            self.SAVED_SEARCH_NAME,
            self.SCHEDULE_NAME,
            self.THRESHOLD_ACTION_NAME,
            parameters
        )

        self.assertTrue(isinstance(result, ScheduleThreshold))

    def test_can_create_webhook(self):
        self.lam_client.saved_searches.create_or_update(
            self.RESOURCE_GROUP,
            self.WORKSPACE_NAME,
            self.SAVED_SEARCH_NAME,
            SavedSearch(self.CATEGORY, self.SAVED_SEARCH_NAME, self.SAMPLE_QUERY, 1)
        )

        self.laa_client.alert_services.create_schedule(
            self.RESOURCE_GROUP,
            self.WORKSPACE_NAME,
            self.SAVED_SEARCH_NAME,
            self.SCHEDULE_NAME,
            SearchSchedule(5, 5, True)
        )

        parameters = ScheduleThreshold(self.THRESHOLD_ACTION_NAME, "Critical", {"operator": "gt", "value": "80"}, {"recipients": ["bob@kelso.co.ed"], "subject": "Test Alert"})

        self.laa_client.alert_services.create_threshold(
            self.RESOURCE_GROUP,
            self.WORKSPACE_NAME,
            self.SAVED_SEARCH_NAME,
            self.SCHEDULE_NAME,
            self.THRESHOLD_ACTION_NAME,
            parameters
        )

        parameters = ScheduleWebhook(self.WEBHOOK_ACTION_NAME, "https://", "{\"test\":\"value\"}")

        result = self.laa_client.alert_services.create_webhook(
            self.RESOURCE_GROUP,
            self.WORKSPACE_NAME,
            self.SAVED_SEARCH_NAME,
            self.SCHEDULE_NAME,
            self.WEBHOOK_ACTION_NAME,
            parameters
        )
        self.assertTrue(isinstance(result, ScheduleWebhook))



