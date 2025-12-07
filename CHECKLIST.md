# Checklist

- [x] Ask top 3 clarifying questions
- [x] Create ai-runner.py script with code_folder variable set to /code/
- [x] Implement logic to check and delete /code/demo-card-app if it exists
- [x] Implement logic to check and copy /code/demo-card-app-orig to /code/demo-card-app if orig exists

## Original User Prompt

I want a python script called "ai-runner.py" in the root of this folder. This python script should
1) first, have a code_folder which is set to /code/
2) check to see if code_folder/demo-card-app folder exists - if it does, then recursively delete it
3) check to see if code_folder/demo-card-app-orig exists - if it does, copy it into code_folder/demo-card-app
