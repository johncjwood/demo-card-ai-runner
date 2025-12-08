# Checklist

- [x] Ask top 3 clarifying questions
- [x] Read the full ai-runner.py file to understand the context
- [x] Fix the FileExistsError for db directory by using dirs_exist_ok parameter
- [x] Ensure testing folder deletion/recreation logic is correct
- [x] Update all instances where db folder is copied

## Original User Prompt

Update ai-runner.py to not have this error.
FileExistsError: [Errno 17] File exists: '/code/demo-card-app/db'

To note, when copying files into the db directory, it should add in new files files, not delete existing ones.

For the testing folder, when copying, it should delete and recreate
