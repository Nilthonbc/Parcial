# 1. Declarar que usaremos el proveedor "local"
terraform {
  required_providers {
    local = {
      source = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

# 2. Definir una variable para el número de build de Jenkins
variable "build_number" {
  type        = string
  description = "Número de la ejecución actual de Jenkins"
  default     = "N/A"
}

# 3. Definir el recurso que queremos crear: un archivo local
resource "local_file" "pipeline_reporte" {
  
  # Contenido del archivo. Usamos la variable de Jenkins.
  content  = "Reporte de ejecución del Pipeline ETL. Build de Jenkins: ${var.build_number}"
  # Nombre del archivo que se creará
  filename = "pipeline_reporte.txt"
}
