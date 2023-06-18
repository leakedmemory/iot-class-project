terraform {
  backend "azurerm" {
    resource_group_name = "terraform_state_rg"
    storage_account_name = "saprojetoiot"
    container_name = "terraform"
    key = "infrastructure.tfstate"
    access_key = "PQDON8erihJNI1BTNEJ0AARK2u2NzbCGIehyTK+pRlxj9Jw7mtTmQVZoECRC8ds52Z25ywQC6+93+ASt7NIEOQ=="
  }
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=3.0.0"
    }
  }
}

provider "azurerm" {
  features {}
}