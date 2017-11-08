# CLI for the Azure Alerting REST API

Provides the ability to create Azure Log Analytics Alerts. There is currently no [Azure Python SDK]("https://github.com/Azure/azure-sdk-for-python/") support for creating Alerts.
This library uses the `azure-mgmt-loganalytics` package for managing Saved Searches.

# Usage

```bash
pip install git+https://github.com/energizedwork/azure-log-analytics-alerts-cli.git
```

The following environment variables need to be set:

* AZURE_TENANT_ID
* AZURE_CLIENT_ID
* AZURE_CLIENT_SECRET
* AZURE_SUBSCRIPTION_ID

List available commands:

```bash
az-la-cli --help
```

To create an alert:

```bash
az-la-cli create-metric-alert 
    --workspace-name "my-oms-workspace" 
    --search-name "my search" 
    --resource-group "rg" 
    --name "Name of My Alert" 
    --threshold-operator "gt" 
    --threshold-value "80" 
    --query "Type=Perf ObjectName=\"Processor\" CounterName=\"% Processor Time\" Computer=\"VM1\" | measure avg(CounterValue) by Computer Interval 5MINUTES"`
```

# More Info

### [Log Analytics API]("https://docs.microsoft.com/en-us/azure/log-analytics/log-analytics-log-search-api")
### [Alert API]("https://docs.microsoft.com/en-us/azure/log-analytics/log-analytics-api-alerts")
