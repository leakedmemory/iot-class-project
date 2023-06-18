resource "azurerm_cosmosdb_account" "projeto_iot" {
  name                = "cosmos-db-${var.PROJECT_NAME}"
  location            = azurerm_resource_group.projeto_iot.location
  resource_group_name = azurerm_resource_group.projeto_iot.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  enable_automatic_failover         = false
  enable_multiple_write_locations   = false
  is_virtual_network_filter_enabled = false
  enable_free_tier = true

  
  consistency_policy {
    consistency_level       = "Session"
    max_interval_in_seconds = 5
    max_staleness_prefix    = 100
  }

  geo_location {
    location          = "eastus"
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_sql_database" "db" {
  name                = "${var.PROJECT_NAME}-sql-db"
  resource_group_name = azurerm_cosmosdb_account.projeto_iot.resource_group_name
  account_name        = azurerm_cosmosdb_account.projeto_iot.name
  

}

resource "azurerm_cosmosdb_sql_container" "access_logs" {
  name                  = "access_logs"
  resource_group_name   = azurerm_cosmosdb_account.projeto_iot.resource_group_name
  account_name          = azurerm_cosmosdb_account.projeto_iot.name
  database_name         = azurerm_cosmosdb_sql_database.db.name
  partition_key_path    = "/id"
  partition_key_version = 1
  throughput            = 400

  indexing_policy {
    indexing_mode = "consistent"

    excluded_path {
      path = "/*"
    }
  }

  conflict_resolution_policy {
    mode                          = "LastWriterWins"
    conflict_resolution_path      = "/_ts"
  }
}

resource "azurerm_cosmosdb_sql_container" "users" {
  name                  = "users"
  resource_group_name   = azurerm_cosmosdb_account.projeto_iot.resource_group_name
  account_name          = azurerm_cosmosdb_account.projeto_iot.name
  database_name         = azurerm_cosmosdb_sql_database.db.name
  partition_key_path    = "/id"
  partition_key_version = 1
  throughput            = 400

  indexing_policy {
    indexing_mode = "consistent"

    excluded_path {
      path = "/*"
    }
  }

  conflict_resolution_policy {
    mode                          = "LastWriterWins"
    conflict_resolution_path      = "/_ts"
  }
}