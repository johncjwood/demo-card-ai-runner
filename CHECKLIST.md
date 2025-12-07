# Checklist

- [x] Ask top 3 clarifying questions
- [x] Read the current RESULTS_FILE format to understand the CSV structure
- [x] Add function to check if smaller L or C level succeeded
- [x] Integrate the check before the test execution in the main loop
- [x] Test the logic to ensure it works correctly

## Original User Prompt

Before the loop starts in the ai-runner.py, check the RESULTS_FILE csv to see if a version of the prompt with a smaller L (prompt) level or smaller C (Context) level succeeded. If so, then skip the test.
