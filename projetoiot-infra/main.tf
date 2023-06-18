module "infra" {
  source = "./infra"

  RESOURCE_GROUP = var.RESOURCE_GROUP
  LOCATION = var.LOCATION
  PROJECT_NAME = var.PROJECT_NAME
}