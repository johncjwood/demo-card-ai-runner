# Checklist

- [x] Ask top 3 clarifying questions
- [x] Add C7 context case to copy_context function
- [x] Copy CLAUDE_CHECKLIST.md, PROJECT.md, and DBScripts.md to .amazonq/rules folder
- [x] Copy run_query.py and schema_search.py to DEMO_APP folder
- [x] Add C8 context case to copy_context function
- [x] Copy all C7 files plus STARTSERVICE.md to .amazonq/rules folder
- [x] Copy start_service.py to DEMO_APP folder
- [x] Add C9 context case to copy_context function
- [x] Copy all C7 files to appropriate locations
- [x] Copy TESTING.md with test command prepended to .amazonq/rules folder
- [x] Copy testing folder to DEMO_APP folder
- [x] Update copy_context signature to accept requirement parameter

## User's Original Prompts

### Prompt 1 (C7):
In copy_context in ai-runner.py, when context=C7:
copy CLAUDE_CHECKLIST.md, PROJECT.md, and DBScripts.md into the .amazonq/rules folder

Also, copy run_query.py and schema_search.py into the DEMO_APP folder

### Prompt 2 (C8):
In copy_context in ai-runner.py, when context=C8:
copy everything we copied in C7.
also copy STARTSERVICE.md into the .amazonq/rules folder

Also, copy start_service.py into the DEMO_APP folder

### Prompt 3 (C9):
In copy_context in ai-runner.py, when context=C9:
copy everything we copied in C7.
also copy TESTING.md into the .amazonq/rules folder
also write, to the top of TESTING.md, the appropriate command from TEST_COMMANDS with the note "this should be what you run to test this prompt"

finally, also copy the entire testing folder into the DEMO_APP folder
