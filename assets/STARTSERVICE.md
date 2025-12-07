# Start Service Script

## Overview

`start_service.py` automates the process of stopping existing Docker containers and rebuilding/starting all services for the card collection application.

## Usage

Run the script from the project root directory:

```bash
python3 start_service.py
```

Or make it executable and run directly:

```bash
chmod +x start_service.py
./start_service.py
```

## What It Does

1. **Stops all running containers** - Executes `docker compose down -v` to stop and remove all containers and volumes
2. **Builds and starts services** - Executes `docker compose up --build -d --remove-orphans` to rebuild images and start all services in detached mode

## Services Started

- **postgres** - PostgreSQL database (port 5432)
- **db-setup** - Database initialization and schema setup
- **rest-api** - REST API backend (port 3001)
- **frontend** - Angular frontend (port 80)

## Prerequisites

- Docker and Docker Compose installed
- Python 3 installed
- Run from the `/code/demo-card-app` directory

## Notes

- The `-v` flag removes volumes, ensuring a clean database state
- The `--build` flag forces rebuild of all images
- The `-d` flag runs containers in detached mode
- The `--remove-orphans` flag removes containers for services not defined in the compose file
