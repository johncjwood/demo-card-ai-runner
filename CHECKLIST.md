# Checklist

- [x] Ask top 3 clarifying questions
- [x] Review existing ai-runner.py structure (if exists)
- [x] Define data structures for Requirements (R1-R7), Levels (L1-L3), and Contexts (C1-C12)
- [x] Implement main loop structure (Requirement -> Level -> Context)
- [x] Implement step 1: Copy demo-card-app-orig to demo-card-app
- [x] Implement step 2: Copy context files based on context level
- [x] Implement step 3: Run AmazonQ CLI with appropriate prompt
- [x] Implement step 4: Enable unsafe mode and log AI output to LOG.txt
- [x] Implement step 5a: Copy test assets (db folder, testing folder, docker-compose.yml)
- [x] Implement step 5b: Run requirement-specific tests
- [x] Implement step 6: Append results to results.csv
- [x] Implement step 7: Rename demo-card-app folder with test results
- [ ] Test the script with a single iteration

## Original User Prompt

The goal of ai-runner.py is to have a process which iteratively runs tests to see if AmazonQ can implement the code correctly and in a single prompt. There are 7 separate requirements, with 3 levels of prompts each. Let's call these 7 requirements R1 - R7 and the 3 levels P1 through P3. To help AmazonQ, we are providing 12 different combinations of context called C1-C12.

The loop for running these tests should be:
For each Requirement:
  for each Level:
      for each Context:

Within this loop, the script should:
1) Make a copy of the demo-card-app-orig into the demo-card-app folder
2) Copy in the relevant context for each context level.
For M1, nothing is copied in. For M2, we copy the ./assets/CLAUDE_PERSONA.md file into demo-card-app's .amazonq/rules folder.
3) Run AmazonQ CLI with the prompt associated with the Requirement and the Level. To start, the R1 & L1 prompt is:
"On the initial page, we see -1 as the total cards. 
Update it to be -2."
The R1 & L2 prompt is:
 "On the dashboard page, the default behavior is to display -1 as the total cards. 
Update it to be -2."

4) While the prompt is running, ensure that AmazonQ can run in unsafe mode and can run any command it wants. Also, all output from the AI should be saved in a LOG.txt file in the demo-card-app folder

5) After the AI runs, then we do the testing. 
5a) First, copy in the contents of the ./assets/db folder into the demo-card-app/db folder. Next, copy the entire ./assets/testing folder into the demo-card-app folder. Also, copy in the docker-compose.yml into the demo-card-app folder.

5b)The tests are unique to each Requirement. For R1, run:
node test-runner.js 100 200 300 310 350 360 390 395 400 500 600 601 901

6) Append the results of the run into the end of the  demo-card-ai-runner folder (the current folder) into results.csv as a comma separated line:
R_, L_, M_, X
where _ is the exact R/L/M test we just ran and X is 1 or 0, where 1 is All tests succeeded and 0 is Any test failed.

7) Finally, move the demo-card-app folder to demo-card-app-R_L_M_X, where the blanks and the X are filled in appropriately
