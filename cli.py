import os
import click

from msrestazure.azure_active_directory import ServicePrincipalCredentials
from azure.mgmt.loganalytics.log_analytics_management_client import LogAnalyticsManagementClient

from azure_log_analytics.azure_log_analytics_api import LogAnalyticsAlertClient

from azure.mgmt.loganalytics.models import SavedSearch
from azure_log_analytics.models.schedule_threshold import ScheduleThreshold
from azure_log_analytics.models.schedule_webhook import ScheduleWebhook
from azure_log_analytics.models.search_schedule import SearchSchedule


def create_clients():
    config = {
        "tenant_id": os.environ.get("AZURE_TENANT"),
        "client_id": os.environ.get("AZURE_CLIENT_ID"),
        "client_secret": os.environ.get("AZURE_SECRET"),
        "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
    }

    for k, v in config.items():
        if not v:
            raise ValueError("'{}' config value not set".format(k))

    credentials = ServicePrincipalCredentials(
        config["client_id"],
        config["client_secret"],
        tenant=config["tenant_id"],
        verify=True,
        resource="https://management.azure.com/"
    )

    alert_client = LogAnalyticsAlertClient(credentials, config["subscription_id"])
    mgmt_client = LogAnalyticsManagementClient(credentials, config["subscription_id"])

    return mgmt_client, alert_client


@click.group()
def cli():
    pass


@cli.command("version")
def version():
    from version import __version__
    click.echo(__version__)


@cli.command("get-search")
@click.option('--workspace-name', help='OMS Workspace Name')
@click.option('--search-name', help='The name of the saved search created for the alert')
@click.option('--resource-group', help='The resource group of the Workspace')
def get_saved_search(workspace_name, search_name, resource_group):
    _mgmt_client, _alert_client = create_clients()

    click.echo("getting saved search")

    result = _mgmt_client.saved_searches.get(resource_group, workspace_name, search_name)

    print(result)


@cli.command("delete-schedule")
@click.option('--workspace-name', help='OMS Workspace Name')
@click.option('--search-name', help='The name of the saved search created for the alert')
@click.option('--resource-group', help='The resource group of the Workspace')
@click.option('--schedule-name', help='The name of the schedule to delete')
def delete_schedule(workspace_name, search_name, resource_group, schedule_name):
    _mgmt_client, _alert_client = create_clients()

    click.echo("deleting schedule")

    result = _alert_client.alert_services.delete_schedule(resource_group, workspace_name, search_name, schedule_name)

    print(result)


@cli.command("delete-threshold")
@click.option('--workspace-name', help='OMS Workspace Name')
@click.option('--search-name', help='The name of the saved search created for the alert')
@click.option('--resource-group', help='The resource group of the Workspace')
@click.option('--schedule-name', help='The name of the schedule')
@click.option('--name', help='The name of the threshold to delete')
def delete_threshold(workspace_name, search_name, resource_group, schedule_name, name):
    _mgmt_client, _alert_client = create_clients()

    click.echo("deleting threshold")

    result = _alert_client.alert_services.delete_threshold(resource_group, workspace_name, search_name, schedule_name, name)

    print(result)


@cli.command("delete-webhook")
@click.option('--workspace-name', help='OMS Workspace Name')
@click.option('--search-name', help='The name of the saved search created for the alert')
@click.option('--resource-group', help='The resource group of the Workspace')
@click.option('--schedule-name', help='The name of the schedule')
@click.option('--name', help='The name of the webhook to delete')
def delete_webhook(workspace_name, search_name, resource_group, schedule_name, name):
    _mgmt_client, _alert_client = create_clients()

    click.echo("deleting webhook")

    result = _alert_client.alert_services.delete_webhook(resource_group, workspace_name, search_name, schedule_name, name)

    print(result)


@cli.command("delete-search")
@click.option('--workspace-name', help='OMS Workspace Name')
@click.option('--search-name', help='The name of the saved search created for the alert')
@click.option('--resource-group', help='The resource group of the Workspace')
def delete_saved_search(workspace_name, search_name, resource_group):
    _mgmt_client, _alert_client = create_clients()

    click.echo("deleting saved search")

    _mgmt_client.saved_searches.delete(resource_group, workspace_name, search_name)


@cli.command("create-alert")
@click.option('--workspace-name', help='OMS Workspace Name')
@click.option('--name', help='The name of the Alert')
@click.option('--search-name', help='The name of the saved search created for the alert')
@click.option('--threshold-operator', help='Comparison operator. e.g gt, lt, eq')
@click.option('--threshold-value', help='Comparison value')
@click.option('--resource-group', help='The resource group of the Workspace')
@click.option('--query', help='The search query used to alert on')
@click.option('--query-interval', help='How frequently the search query is run', default=5)
@click.option('--query-timespan', help='The timespan of data to evaluate', default=5)
@click.option('--alert-email-recipient', default="")
@click.option('--alert-webhook-uri', default="")
@click.option('--alert-webhook-payload', default="")
def create_metric_alert(workspace_name, name, search_name, threshold_operator, threshold_value, resource_group, query, query_interval, query_timespan, alert_email_recipient, alert_webhook_uri, alert_webhook_payload):
    _mgmt_client, _alert_client = create_clients()

    search_parameters = SavedSearch("Alert Queries", search_name, query, 1)

    try:
        click.echo("creating search {}".format(search_name))
        _mgmt_client.saved_searches.create_or_update(resource_group, workspace_name, search_name, search_parameters)
    except AttributeError as e:
        if e.args[0] == "'NoneType' object has no attribute 'error'":
            click.echo("Error '409 Conflict'. The resource already exists. Resource updates not supported.")
        else:
            raise e

    schedule_params = SearchSchedule(query_interval, query_timespan, True)
    schedule_name = "{}-schedule".format(search_name)

    click.echo("creating schedule {}".format(schedule_name))
    _alert_client.alert_services.create_schedule(resource_group, workspace_name, search_name, schedule_name, schedule_params)

    threshold_name = "{}-action-threshold".format(search_name)
    threshold_params = ScheduleThreshold(
        threshold_name,
        "critical",
        {"operator": threshold_operator, "value": threshold_value},
        {"recipients": [alert_email_recipient], "subject": name}
    )

    click.echo("creating threshold {}".format(threshold_name))
    _alert_client.alert_services.create_threshold(resource_group, workspace_name, search_name, schedule_name, threshold_name, threshold_params)

    webhook_name = "{}-action-webhook".format(search_name)
    webhook_params = ScheduleWebhook(
        webhook_name,
        alert_webhook_uri,
        alert_webhook_payload
    )

    click.echo("creating webhook {}".format(webhook_name))
    result = _alert_client.alert_services.create_webhook(resource_group, workspace_name, search_name, schedule_name, webhook_name, webhook_params)

    print(result)


if __name__ == "__main__":
    cli()
