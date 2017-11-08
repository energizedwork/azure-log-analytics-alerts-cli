import os
import click

from msrestazure.azure_active_directory import ServicePrincipalCredentials
from azure.mgmt.loganalytics.log_analytics_management_client import LogAnalyticsManagementClient
from azure_log_analytics.azure_log_analytics_api import LogAnalyticsAlertClient

from azure.mgmt.loganalytics.models import SavedSearch
from azure_log_analytics.models.schedule_threshold import ScheduleThreshold
from azure_log_analytics.models.schedule_webhook import ScheduleWebhook
from azure_log_analytics.models.search_schedule import SearchSchedule


CONFIG = {
    "tenant_id": os.environ.get("AZURE_TENANT_ID"),
    "client_id": os.environ.get("AZURE_CLIENT_ID"),
    "client_secret": os.environ.get("AZURE_CLIENT_SECRET"),
    "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
}

for k, v in CONFIG.items():
    if not v:
        raise ValueError("'{}' config value not set".format(k))

CREDENTIALS = ServicePrincipalCredentials(
    CONFIG["client_id"],
    CONFIG["client_secret"],
    tenant=CONFIG["tenant_id"],
    verify=True,
    resource="https://management.azure.com/"
)

LA_ALERT_CLIENT = LogAnalyticsAlertClient(CREDENTIALS, CONFIG["subscription_id"])
LA_MGMT_CLIENT = LogAnalyticsManagementClient(CREDENTIALS, CONFIG["subscription_id"])


@click.group()
def cli():
    pass


@cli.command("get-search")
@click.option('--workspace-name', help='OMS Workspace Name')
@click.option('--search-name', help='The name of the saved search created for the alert')
@click.option('--resource-group', help='The resource group of the Workspace')
def get_saved_search(workspace_name, search_name, resource_group):
    click.echo("getting saved search")

    result = LA_MGMT_CLIENT.saved_searches.get(resource_group, workspace_name, search_name)

    print(result)


@cli.command("delete-schedule")
@click.option('--workspace-name', help='OMS Workspace Name')
@click.option('--search-name', help='The name of the saved search created for the alert')
@click.option('--resource-group', help='The resource group of the Workspace')
@click.option('--schedule-name', help='The name of the schedule to delete')
def delete_search_schedule(workspace_name, search_name, resource_group, schedule_name):
    click.echo("deleting search schedule")

    result = LA_ALERT_CLIENT.alert_services.delete_search_schedule(resource_group, workspace_name, search_name, schedule_name)

    print(result)


@cli.command("delete-search")
@click.option('--workspace-name', help='OMS Workspace Name')
@click.option('--search-name', help='The name of the saved search created for the alert')
@click.option('--resource-group', help='The resource group of the Workspace')
def delete_saved_search(workspace_name, search_name, resource_group):
    click.echo("deleting saved search")

    LA_MGMT_CLIENT.saved_searches.delete(resource_group, workspace_name, search_name)


@cli.command("create-alert")
@click.option('--workspace-name', help='OMS Workspace Name')
@click.option('--name', help='The name of the Alert')
@click.option('--search-name', help='The name of the saved search created for the alert')
@click.option('--threshold-operator', help='Comparison operator. e.g gt, lt, eq')
@click.option('--threshold-value', help='Comparison value')
@click.option('--resource-group', help='The resource group of the Workspace')
@click.option('--query', help='The search query used to alert on')
def create_metric_alert(workspace_name, name, search_name, threshold_operator, threshold_value, resource_group, query):
    search_parameters = SavedSearch("Alert Queries", search_name, query, 1)

    try:
        click.echo("creating search {}".format(search_name))
        LA_MGMT_CLIENT.saved_searches.create_or_update(resource_group, workspace_name, search_name, search_parameters)
    except AttributeError as e:
        if e.args[0] == "'NoneType' object has no attribute 'error'":
            click.echo("Error '409 Conflict'. The resource already exists. Resource updates not supported.")
        else:
            raise e

    schedule_params = SearchSchedule(5, 5, True)

    click.echo("creating schedule")
    LA_ALERT_CLIENT.alert_services.create_schedule(resource_group, workspace_name, search_name, "{}-schedule".format(search_name), schedule_params)

    threshold_params = ScheduleThreshold(
        "{}-action-threshold".format(search_name),
        "critical",
        {"operator": threshold_operator, "value": threshold_value},
        {"recipients": ["ops-alerts@energizedwork.com"], "subject": name}
    )

    click.echo("creating threshold for {}".format(name))
    LA_ALERT_CLIENT.alert_services.create_threshold(resource_group, workspace_name, search_name, threshold_params.name, name, threshold_params)

    webhook_params = ScheduleWebhook(
        "{}-action-threshold".format(search_name),
        "https://hooks.slack.com/services/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",
        "{\"channel\": \"#ey-mobility-ops\", \"username\": \"Azure Log Analytics\", \"text\": \"%s\", \"icon_emoji\": \":warning:\"}" % name
    )

    click.echo("creating webhook for {}".format(name))
    result = LA_ALERT_CLIENT.alert_services.create_webhook(resource_group, workspace_name, search_name, "{}-schedule".format(search_name), webhook_params.name, webhook_params)

    print(result)


if __name__ == "__main__":
    cli()
