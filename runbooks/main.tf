terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

resource "docker_image" "observai" {
  name = "observai-app:latest"
  build {
    path = "."
  }
}

resource "docker_container" "observai" {
  image = docker_image.observai.image
  name  = "observai-container"
  ports {
    internal = 8080
    external = 8080
  }
}