resource "azurerm_servicebus_namespace" "projeto_iot" {
  name                = "sb-${var.PROJECT_NAME}"
  location            = azurerm_resource_group.projeto_iot.location
  resource_group_name = azurerm_resource_group.projeto_iot.name
  sku                 = "Standard"
}

resource "azurerm_servicebus_queue" "access_log" {
  name         = "sbq-access-log"
  namespace_id = azurerm_servicebus_namespace.projeto_iot.id
}