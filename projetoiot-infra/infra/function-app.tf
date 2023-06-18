resource "azurerm_storage_account" "function_app" {
  name                     = "sa${var.PROJECT_NAME}app"
  resource_group_name      = azurerm_resource_group.projeto_iot.name
  location                 = azurerm_resource_group.projeto_iot.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "function_app" {
  name                = "${var.PROJECT_NAME}-service-plan"
  resource_group_name = azurerm_resource_group.projeto_iot.name
  location            = azurerm_resource_group.projeto_iot.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_application_insights" "linux" {
  name                = "${var.PROJECT_NAME}-linux-function-app"
  resource_group_name = azurerm_resource_group.projeto_iot.name
  location            = azurerm_resource_group.projeto_iot.location
  application_type    = "web"
}

resource "azurerm_linux_function_app" "linux" {
  name                = "${var.PROJECT_NAME}-linux-function-app"
  resource_group_name = azurerm_resource_group.projeto_iot.name
  location            = azurerm_resource_group.projeto_iot.location

  storage_account_name       = azurerm_storage_account.function_app.name
  storage_account_access_key = azurerm_storage_account.function_app.primary_access_key
  service_plan_id            = azurerm_service_plan.function_app.id

  site_config {
    application_insights_connection_string = azurerm_application_insights.linux.connection_string
    application_insights_key               = azurerm_application_insights.linux.instrumentation_key

    application_stack {
      python_version = "3.10"
    }
  }
  
  app_settings = {
    ACCOUNT_URI = azurerm_cosmosdb_account.projeto_iot.endpoint
    ACCOUNT_KEY = azurerm_cosmosdb_account.projeto_iot.primary_key
    DATABASE_NAME = azurerm_cosmosdb_sql_database.db.name
    USERS_CONTAINER = azurerm_cosmosdb_sql_container.users.name
    LOGS_CONTAINER = azurerm_cosmosdb_sql_container.access_logs.name
    SERVICE_BUS_CONNECTION = azurerm_servicebus_namespace.projeto_iot.default_primary_connection_string
    SERVICE_BUS_QUEUE_NAME = azurerm_servicebus_queue.access_log.name
    AZURE_STORAGE_IMAGES_CONNECTION_STRING = azurerm_storage_account.images.primary_connection_string
    AZURE_STORAGE_IMAGES_PRIMARY_KEY = azurerm_storage_account.images.primary_access_key
  }

  lifecycle {
    ignore_changes = [
      tags
    ]
  }
}