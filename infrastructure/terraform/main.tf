provider "azurerm" {
  features {}
}

provider "aws" {
  region = var.aws_region
}

resource "azurerm_resource_group" "migration" {
  name     = "rg-${var.project_name}-migration-${var.environment}"
  location = var.location
}

# --- Migration Control Plane (AKS) ---

resource "azurerm_kubernetes_cluster" "migration_k8s" {
  name                = "aks-migration-iq-${var.environment}"
  location            = azurerm_resource_group.migration.location
  resource_group_name = azurerm_resource_group.migration.name
  dns_prefix          = "migration-k8s"

  default_node_pool {
    name       = "default"
    node_count = 3
    vm_size    = "Standard_D2s_v3"
  }

  identity {
    type = "SystemAssigned"
  }
}

# --- Migration Metadata Store (Postgres) ---

resource "azurerm_postgresql_flexible_server" "metadata" {
  name                   = "psql-migration-metadata-${var.environment}"
  resource_group_name    = azurerm_resource_group.migration.name
  location               = azurerm_resource_group.migration.location
  version                = "13"
  administrator_login    = "migadmin"
  administrator_password = var.db_password
  storage_mb             = 32768
  sku_name               = "GP_Standard_D2ds_v4"
}

# --- Event Queue (Redis) ---

resource "azurerm_redis_cache" "queue" {
  name                = "redis-migration-queue-${var.environment}"
  location            = azurerm_resource_group.migration.location
  resource_group_name = azurerm_resource_group.migration.name
  capacity            = 1
  family              = "C"
  sku_name            = "Standard"
  enable_non_ssl_port = false
}

# --- Multi-Cloud Transit (AWS S3 Migration Target) ---

resource "aws_s3_bucket" "migration_staging" {
  bucket = "db-migration-staging-${var.environment}"
}
