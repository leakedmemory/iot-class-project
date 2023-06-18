resource "azurerm_storage_account" "images" {
  name                     = "sa${var.PROJECT_NAME}images"
  resource_group_name      = azurerm_resource_group.projeto_iot.name
  location                 = azurerm_resource_group.projeto_iot.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "users" {
  name                  = "users"
  storage_account_name  = azurerm_storage_account.images.name
  container_access_type = "blob"
}

resource "azurerm_storage_container" "access" {
  name                  = "access"
  storage_account_name  = azurerm_storage_account.images.name
  container_access_type = "blob"
}