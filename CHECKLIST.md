# Checklist

- [x] Ask top 3 clarifying questions
- [x] Read ai-runner.py to understand current implementation
- [x] Locate stop_all_docker() function and docker-compose.yml check logic
- [x] Add docker-compose.yml detection after stop_all_docker()
- [x] Add docker compose rebuild command with proper flags
- [x] Add database readiness check before proceeding
- [x] Test the changes

## Original User Prompt

In the ai-runner.py, if you see the docker-compose.yml file after running stop_all_docker(), then run 

docker compose down -v && docker compose up --build -d --remove-orphans

Ensure that the database is up before going onto the next step
