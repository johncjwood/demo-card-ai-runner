import os
import shutil
import subprocess
import sys
import time
import requests

# Configuration
Q_BIN_FOLDER = "/home/john/.local/bin/"
CODE_FOLDER = "/code/"
DEMO_APP = os.path.join(CODE_FOLDER, "demo-card-app")
DEMO_APP_ORIG = os.path.join(CODE_FOLDER, "demo-card-app-orig")
RUNNER_FOLDER = "/code/demo-card-ai-runner"
ASSETS_FOLDER = os.path.join(RUNNER_FOLDER, "assets")
RESULTS_FILE = os.path.join(RUNNER_FOLDER, "results.csv")

# Define prompts for each requirement and level
PROMPTS = {
    "R0": {"L1": "No prompt.", "L2": "No prompt.", "L3": "No prompt."},
    "R1": {
        "L1": "On the initial page, we see -1 as the total cards. \nUpdate it to be -2.",
        "L2": """On the dashboard page, the default behavior is to display -1 as the total cards. 
        \nUpdate it to be -2."""
        ,"L3": """On the /dashboard page in the Angular code in the ./frontend folder, 
        the default placeholder in dashboard.component.ts for the total cards is -1. 
        \nUpdate the default placeholder from -1 to be -2."""
    },
    "R2": {"L1": """
On the initial page, we see -1 as the total cards. 
Update it to be the real amount.
"""
           , "L2": """
I'm working on the dashboard component and noticed it's hardcoded to show -1 for total cards. I need to:

Create an API endpoint in the Node.js backend that queries the database for the card count

Update the Angular dashboard component to call this new endpoint

Display the returned count in the UI instead of the -1 placeholder
I think I need to modify the service layer on the frontend and add a new route in the REST API, but I'm not sure which specific files handle the dashboard data.
"""
           , "L3": """
The DashboardComponent is rendering a hardcoded -1 value for totalCards. Need to implement proper card count aggregation:

Backend:

Add GET /api/cards/count endpoint in the Express router

Implement COUNT(*) query against the cards table in PostgreSQL

Return JSON response with total count

Frontend:

Update CardService (or equivalent data service) to add getCardCount() method that hits the new endpoint

Modify DashboardComponent ngOnInit() lifecycle hook to subscribe to the Observable

Bind the response to the totalCards property for template interpolation

Files likely affected: rest/src/routes/cards.js, rest/src/controllers/cardsController.js, frontend/src/app/services/card.service.ts, frontend/src/app/dashboard/dashboard.component.ts
"""
           }
    ,"R3": {"L1": """
the shopping cart thing is letting people add way more cards than we actually have lol. like if someone just keeps clicking the plus button they can add infinite cards even tho we only have like 5 in stock or whatever. can you make it stop doing that? 
it should probably just not let them add more once they hit the max we have
"""
           , "L2": """
There's a bug in the cart functionality where users can increment item quantities beyond available inventory. 
The frontend increment button doesn't check against the inventory count from the backend before updating the cart state. 
We need to add validation so that when a user clicks the + button on a card in the cart, it checks the inventory table and prevents the cart quantity from exceeding the available stock. 
This should involve updating the cart component logic and possibly the API endpoint that handles cart updates.
"""
           , "L3": """
The cart component's increment handler lacks inventory constraint validation. Need to implement a check in the CartService's updateQuantity method that queries the cards table's inventory_count column before allowing increments. 
The Angular cart component should stop incrementing the quantity when cart_items.quantity would exceed cards.inventory_count. This requires:

Modifying the PUT /api/cart/items/:id endpoint to return 400 when requested quantity > inventory
Updating the CartComponent's incrementItem() method to handle this validation response
Optionally, enriching the GET /api/cart response to include available_inventory per item for client-side button state management
Consider race conditions if multiple users are checking out simultaneously
"""
           }
    ,"R4": {"L1": """
hey so the tax thing on checkout isn't right... it's just doing 5% for everyone but it should be different based on where people live. can you make it so it checks what state they're in and does the tax differently? like some states should be 10% (the expensive ones like california and new york and stuff) and the rest should be 7%. 
the state info should be somewhere in their profile i think
"""
           , "L2": """
I need to update the checkout page tax calculation logic. Currently it's hardcoded to 5%, but we need to make it dynamic based on the user's state.

Here's what needs to happen:
- The frontend checkout component needs to get the user's state from their profile
- We'll need to add logic (probably in the API layer) to calculate tax based on state
- For CA, MA, NY, NC, and IL → use 10% tax rate
- For all other states → use 7% tax rate

I think this will involve updating the checkout component, maybe adding a new API endpoint or modifying an existing one, and possibly updating the user profile query to include the state field. The tax calculation should probably happen on the backend to keep it secure.

"""
           , "L3": """
Refactor the tax calculation logic in the checkout flow to implement state-based tax rates:

**Backend Changes:**
- Modify the checkout API endpoint (likely POST /api/checkout or /api/orders) in the Express route handler
- Add a JOIN to the user profile query to retrieve the `state` column from the `users` or `user_profiles` table
- Implement tax rate calculation logic: HIGH_TAX_STATES = ['CA', 'MA', 'NY', 'NC', 'IL'] → 0.10, DEFAULT → 0.07
- Update the order calculation service to apply the dynamic tax rate instead of the hardcoded 0.05

**Frontend Changes:**
- Update the CheckoutComponent to ensure the tax rate displayed reflects the backend calculation
- Remove any hardcoded 5% tax rate constants from the component TypeScript and template
- Ensure the order summary properly binds to the tax amount returned from the API response

**Database:**
- Verify the `state` column exists in the user profile schema (likely `user_profiles.state` or `users.state`)
- If missing, add migration to `./db/99 Additional.sql` to add the column

The tax calculation should be server-authoritative to prevent client-side manipulation.
"""
           }
    ,"R5": {"L1": """
Hey, so like... we need another goal thing? Right now there's just the one that counts all the cards, but I want one that only counts the different ones, not duplicates or whatever. Can you make it show up in that dropdown menu where you pick the goal type? And then make sure it actually works when you add it - like the percentage bar should be right and stuff. 
Oh and the dashboard needs to know about it too for the completed goals counter thing.
"""
           , "L2": """
We need to add a new goal type called 'Total Unique' that counts unique cards instead of total cards. Here's what needs to happen:

Update the frontend dropdown component to include the new goal type option

Add the calculation logic in the backend API endpoint that processes goals

Make sure the Goals page displays the progress percentage correctly when rendering this goal type

Update the Dashboard component so it counts completed goals properly with this new type

I think we'll need to modify the goal service on the backend, update the Angular component that has the dropdown, and maybe adjust the database query to use COUNT(DISTINCT) or something similar.
"""
           , "L3": """
Implement a new goal_type enum value 'total_unique' for distinct card collection tracking. Required changes:

Database Layer:

Add 'total_unique' to goal_type enum in the goals table schema

Implement COUNT(DISTINCT card_id) aggregation in the goal calculation query

REST API (Node.js):

Update GoalService.calculateProgress() method to handle 'total_unique' case with distinct card count logic

Modify GET /api/goals endpoint response to include correct progress calculation

Ensure POST /api/goals validation accepts the new goal_type

Frontend (Angular):

Add 'total_unique' option to the GoalType enum/interface

Update goal-form.component.ts dropdown options array

Modify goals.component.ts to render progress bars using the API-calculated percentage

Update dashboard.component.ts aggregation logic for completed goals count to include 'total_unique' type in the filter

The calculation should query user_cards table with SELECT COUNT(DISTINCT card_id) WHERE user_id = ? and compare against the goal target value.
"""
           }
    ,"R6": {"L1": """
hey so i want to add a new goal thing that counts cards that have like 4 or more of something? it should be called 'Total Above 4' or whatever. basically i need it to show up in that dropdown where you pick the goal type, and then it needs to actually work and count right. oh and make sure it shows up on the goals page with the percentage bar thing, and also the dashboard needs to update when goals are done. thanks!
"""
           , "L2": """
I need to implement a new goal type feature called 'Total Above 4' that counts cards with a minimum count of 4. Here's what needs to happen:

Add 'Total Above 4' as an option in the Goal Type dropdown on the frontend

Write the calculation logic in the backend API to count cards where count >= 4

Make sure the Goals page displays the new goal card with the progress percentage calculated correctly

Update the Dashboard page so it shows the correct number of completed goals including this new type

I think this will involve changes to the Angular components for the dropdown and pages, the Node.js API endpoints for the calculation, and probably the database to store the new goal type.
"""
           , "L3": """
Implement a new GoalType enum value 'TOTAL_ABOVE_4' with the following requirements:

Database Layer:

Insert new goal_type record in the goal_types table via ./db/99 Additional.sql

Ensure goal_type_id and display_name ('Total Above 4') are properly defined

Backend (Node.js/Express):

Update GoalType enum/constants in the goals service/model

Modify the calculateGoalProgress function to handle TOTAL_ABOVE_4 logic: SELECT COUNT(*) FROM cards WHERE count >= 4

Ensure GET /api/goals and GET /api/goals/:id endpoints return correct current_value and progress_percentage

Verify POST /api/goals accepts the new goal type

Frontend (Angular):

Update the GoalType enum in goal.model.ts or equivalent TypeScript interface

Modify the goal-form component's goalTypes array to include the new option for the mat-select/dropdown

Ensure the goals-list component's progress calculation and mat-progress-bar rendering handles the new type

Verify the dashboard component's getCompletedGoalsCount() method correctly aggregates goals where progress_percentage >= 100

All changes should maintain type safety across the full stack and follow existing patterns for goal type implementations.
"""
           }
    ,"R7": {"L1": """
hey so i want to add like a star thing next to people's names when they buy a lot of stuff. like if someone spends over 100 bucks they should get a cool star or something to show they're special. can you make that happen? it should show up on their profile page
"""
           , "L2": """
I need to implement a VIP badge feature for the user profile component. The requirement is to display a star icon next to the username when a user's total purchase amount exceeds $100.

For the frontend, I'll need to update the profile component to conditionally render the star SVG. The backend API should return the total purchase amount with the user data so the frontend can determine whether to show the star. I think we'll also need to query the database to calculate the sum of all purchases for each user.
"""
           , "L3": """
Implement VIP status indicator with the following specifications:

Database Layer:

Add computed field or view to aggregate purchases.amount by user_id where SUM(amount) > 100

REST API:

Extend the user profile endpoint (likely /api/users/:id) response schema to include isVip: boolean or totalPurchases: number

Implement business logic in the user service to calculate VIP eligibility

Angular Frontend:

Update the user profile component template to conditionally render <svg data-icon="star"> adjacent to the username binding

Add *ngIf directive checking the isVip property from the user model

Position the SVG using flexbox with appropriate margin-right spacing

Ensure the component's TypeScript interface includes the new VIP field from the API response
"""
           }
}

# Define test commands for each requirement
TEST_COMMANDS = {
    "R0": "node test-runner.js 100 200 300 310 350 360 390 395 400 500 600 601 900",
    "R1": "node test-runner.js 100 200 300 310 350 360 390 395 400 500 600 601 901",
    "R2": "node test-runner.js 100 200 300 310 350 360 390 395 400 500 600 601 902",
    "R3": "node test-runner.js 100 200 300 310 351 361 390 395 401 500 600 601 900",
    "R4": "node test-runner.js 100 200 300 310 350 362 390 395 400 500 600 601 900",
    "R5": "node test-runner.js 100 200 300 310 350 360 390 395 400 500 600 601 650 651 900",
    "R6": "node test-runner.js 100 200 300 310 350 360 390 395 400 500 600 601 660 661 900",
    "R7": "node test-runner.js 100 200 300 310 350 360 390 395 400 500 600 601 900 950"
}

# Define contexts
CONTEXTS = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]

def copy_demo_app():
    """Step 1: Copy demo-card-app-orig to demo-card-app"""
    if os.path.exists(DEMO_APP):
        shutil.rmtree(DEMO_APP)
    if os.path.exists(DEMO_APP_ORIG):
        shutil.copytree(DEMO_APP_ORIG, DEMO_APP)

def copy_context(context, requirement=None):
    """Step 2: Copy context files based on context level"""
    if context == "C1":
        pass  # Nothing to copy for C1
    elif context == "C2":
        rules_folder = os.path.join(DEMO_APP, ".amazonq", "rules")
        os.makedirs(rules_folder, exist_ok=True)
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "CLAUDE_PERSONA.md"),
            os.path.join(rules_folder, "CLAUDE_PERSONA.md")
        )
    elif context == "C3":
        rules_folder = os.path.join(DEMO_APP, ".amazonq", "rules")
        os.makedirs(rules_folder, exist_ok=True)
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "CLAUDE_CHECKLIST.md"),
            os.path.join(rules_folder, "CLAUDE_CHECKLIST.md")
        )
    elif context == "C4":
        rules_folder = os.path.join(DEMO_APP, ".amazonq", "rules")
        os.makedirs(rules_folder, exist_ok=True)
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "CLAUDE_CHECKLIST.md"),
            os.path.join(rules_folder, "CLAUDE_CHECKLIST.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "PROJECT.md"),
            os.path.join(rules_folder, "PROJECT.md")
        )
    elif context == "C5":
        rules_folder = os.path.join(DEMO_APP, ".amazonq", "rules")
        os.makedirs(rules_folder, exist_ok=True)
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "CLAUDE_CHECKLIST.md"),
            os.path.join(rules_folder, "CLAUDE_CHECKLIST.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "PROJECT.md"),
            os.path.join(rules_folder, "PROJECT.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "CTAS.sql"),
            os.path.join(rules_folder, "CTAS.sql")
        )
    elif context == "C6":
        rules_folder = os.path.join(DEMO_APP, ".amazonq", "rules")
        os.makedirs(rules_folder, exist_ok=True)
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "CLAUDE_CHECKLIST.md"),
            os.path.join(rules_folder, "CLAUDE_CHECKLIST.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "PROJECT.md"),
            os.path.join(rules_folder, "PROJECT.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "DBConnect.md"),
            os.path.join(rules_folder, "DBConnect.md")
        )
    elif context == "C7":
        rules_folder = os.path.join(DEMO_APP, ".amazonq", "rules")
        os.makedirs(rules_folder, exist_ok=True)
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "CLAUDE_CHECKLIST.md"),
            os.path.join(rules_folder, "CLAUDE_CHECKLIST.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "PROJECT.md"),
            os.path.join(rules_folder, "PROJECT.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "DBScripts.md"),
            os.path.join(rules_folder, "DBScripts.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "run_query.py"),
            os.path.join(DEMO_APP, "run_query.py")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "schema_search.py"),
            os.path.join(DEMO_APP, "schema_search.py")
        )
    elif context == "C8":
        rules_folder = os.path.join(DEMO_APP, ".amazonq", "rules")
        os.makedirs(rules_folder, exist_ok=True)
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "CLAUDE_CHECKLIST.md"),
            os.path.join(rules_folder, "CLAUDE_CHECKLIST.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "PROJECT.md"),
            os.path.join(rules_folder, "PROJECT.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "DBScripts.md"),
            os.path.join(rules_folder, "DBScripts.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "STARTSERVICE.md"),
            os.path.join(rules_folder, "STARTSERVICE.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "run_query.py"),
            os.path.join(DEMO_APP, "run_query.py")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "schema_search.py"),
            os.path.join(DEMO_APP, "schema_search.py")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "start_service.py"),
            os.path.join(DEMO_APP, "start_service.py")
        )
    elif context == "C9":
        rules_folder = os.path.join(DEMO_APP, ".amazonq", "rules")
        os.makedirs(rules_folder, exist_ok=True)
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "CLAUDE_CHECKLIST.md"),
            os.path.join(rules_folder, "CLAUDE_CHECKLIST.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "PROJECT.md"),
            os.path.join(rules_folder, "PROJECT.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "DBScripts.md"),
            os.path.join(rules_folder, "DBScripts.md")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "run_query.py"),
            os.path.join(DEMO_APP, "run_query.py")
        )
        shutil.copy(
            os.path.join(ASSETS_FOLDER, "schema_search.py"),
            os.path.join(DEMO_APP, "schema_search.py")
        )
        # Copy TESTING.md with test command prepended
        testing_md_src = os.path.join(ASSETS_FOLDER, "TESTING.md")
        testing_md_dst = os.path.join(rules_folder, "TESTING.md")
        with open(testing_md_src, "r") as src:
            content = src.read()
        test_cmd = TEST_COMMANDS.get(requirement, "")
        with open(testing_md_dst, "w") as dst:
            dst.write(f"# Test Command\n\nThis should be what you run to test this prompt:\n```\n{test_cmd}\n```\n\n")
            dst.write(content)
        # Copy testing folder
        testing_src = os.path.join(ASSETS_FOLDER, "testing")
        testing_dst = os.path.join(DEMO_APP, "testing")
        if os.path.exists(testing_dst):
            shutil.rmtree(testing_dst)
        shutil.copytree(testing_src, testing_dst)

def stop_all_docker():
    """Stop all running docker containers"""
    subprocess.run(
        "docker stop $(docker ps -q)",
        shell=True,
        capture_output=True
    )

def rebuild_docker_if_exists():
    """Rebuild docker services if docker-compose.yml exists"""
    docker_compose_path = os.path.join(DEMO_APP, "docker-compose.yml")
    if os.path.exists(docker_compose_path):
        print("Found docker-compose.yml, rebuilding services...")
        subprocess.run(
            "docker compose down -v && docker compose up --build -d --remove-orphans",
            shell=True,
            cwd=DEMO_APP,
            capture_output=True
        )
        wait_for_database()

def wait_for_database():
    """Wait for database to be ready"""
    print("Waiting for database to be ready...")
    db_retries = 10
    while db_retries > 0:
        try:
            response = requests.post(
                'http://localhost:3001/api/login',
                headers={'Content-Type': 'application/json'},
                json={'username': 'bob', 'password': 'password'},
                timeout=5
            )
            if response.text == '0':
                print("Database is ready")
                return
        except:
            pass
        time.sleep(3)
        db_retries -= 1
    print("Warning: Database may not be ready")

def run_amazonq(prompt):
    """Step 3 & 4: Run AmazonQ CLI with prompt, log output"""
    log_file = os.path.join(DEMO_APP, "LOG.txt")
    
    # AmazonQ CLI command
    q_cmd = os.path.join(Q_BIN_FOLDER, "q")
    cmd = [q_cmd, "chat", "--trust-all-tools", "--no-interactive", prompt]
    
    # Inherit environment and add Q_FAKE_IS_REMOTE if needed
    env = os.environ.copy()
    env["Q_FAKE_IS_REMOTE"] = "1"
    
    with open(log_file, "w") as f:
        f.write(f"{prompt}\n\n")
        result = subprocess.run(
            cmd,
            cwd=DEMO_APP,
            stdout=f,
            stderr=subprocess.STDOUT,
            text=True,
            env=env
        )
    
    return result.returncode == 0

def copy_test_assets():
    """Step 5a: Copy test assets"""
    # Copy db folder contents
    db_src = os.path.join(ASSETS_FOLDER, "db")
    db_dst = os.path.join(DEMO_APP, "db")
    if os.path.exists(db_dst):
        shutil.rmtree(db_dst)
    shutil.copytree(db_src, db_dst)
    
    # Copy testing folder
    testing_src = os.path.join(ASSETS_FOLDER, "testing")
    testing_dst = os.path.join(DEMO_APP, "testing")
    if os.path.exists(testing_dst):
        shutil.rmtree(testing_dst)
    shutil.copytree(testing_src, testing_dst)
    
    # Copy docker-compose.yml
    shutil.copy(
        os.path.join(ASSETS_FOLDER, "docker-compose.yml"),
        os.path.join(DEMO_APP, "docker-compose.yml")
    )

def run_tests(requirement):
    """Step 5b: Run requirement-specific tests"""
    test_cmd = TEST_COMMANDS.get(requirement, "")
    if not test_cmd:
        return False
    
    result = subprocess.run(
        test_cmd,
        shell=True,
        cwd=os.path.join(DEMO_APP, "testing"),
        capture_output=True,
        text=True
    )
    
    # Append test results to log file
    log_file = os.path.join(DEMO_APP, "LOG.txt")
    with open(log_file, "a") as f:
        f.write("\n\n=== TEST RESULTS ===\n")
        f.write(f"Command: {test_cmd}\n")
        f.write(f"Exit Code: {result.returncode}\n")
        f.write(f"Output:\n{result.stdout}\n")
        if result.stderr:
            f.write(f"Errors:\n{result.stderr}\n")
    
    # Tear down docker environment
    subprocess.run(
        "docker-compose down",
        shell=True,
        cwd=DEMO_APP,
        capture_output=True
    )
    
    # Check if all tests succeeded - test-runner.js exits with code 1 on failure
    return result.returncode == 0

def load_results():
    """Load existing results from CSV"""
    results = {}
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    req, lvl, ctx, success = parts
                    results[(req, lvl, ctx)] = int(success)
    return results

def should_skip(requirement, level, context, results):
    """Check if test should be skipped based on smaller L or C success"""
    level_order = ["L1", "L2", "L3"]
    context_order = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
    
    current_level_idx = level_order.index(level)
    current_context_idx = context_order.index(context)
    
    # Check any smaller (L, C) combination
    for i in range(current_level_idx + 1):
        for j in range(current_context_idx + 1):
            if i < current_level_idx or j < current_context_idx:
                if results.get((requirement, level_order[i], context_order[j])) == 1:
                    return True
    
    return False

def append_results(requirement, level, context, success):
    """Step 6: Append results to results.csv"""
    result_value = 1 if success else 0
    with open(RESULTS_FILE, "a") as f:
        f.write(f"{requirement},{level},{context},{result_value}\n")

def rename_demo_app(requirement, level, context, success):
    """Step 7: Rename demo-card-app folder"""
    result_value = 1 if success else 0
    new_name = f"demo-card-app-{requirement}_{level}_{context}_{result_value}"
    new_path = os.path.join(CODE_FOLDER, new_name)
    
    if os.path.exists(new_path):
        shutil.rmtree(new_path)
    
    shutil.move(DEMO_APP, new_path)

def main():
    requirements = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "R7"]
    levels = ["L1", "L2", "L3"]
    
    # Load existing results once at the start
    results = load_results()
    
    for requirement in requirements:
        for level in levels:
            for context in CONTEXTS:
                prompt = PROMPTS[requirement][level]
                
                # Skip if prompt is not defined
                if not prompt:
                    print(f"Skipping {requirement}/{level}/{context} - no prompt defined")
                    continue
                
                # Skip if smaller L or C level succeeded
                if should_skip(requirement, level, context, results):
                    print(f"Skipping {requirement}/{level}/{context} - smaller L or C succeeded")
                    continue
                
                print(f"Running {requirement}/{level}/{context}...")
                
                # Step 1: Copy demo app
                copy_demo_app()
                
                # Step 2: Copy context
                copy_context(context, requirement)
                
                # Step 2.5: Stop all docker containers
                stop_all_docker()
                
                # Step 2.6: Rebuild docker if docker-compose.yml exists
                rebuild_docker_if_exists()
                
                # Step 3 & 4: Run AmazonQ
                run_amazonq(prompt)
                
                # Step 5a: Copy test assets
                copy_test_assets()
                
                # Step 5b: Run tests
                success = run_tests(requirement)
                
                # Step 6: Append results
                append_results(requirement, level, context, success)
                
                # Update in-memory results
                results[(requirement, level, context)] = 1 if success else 0
                
                # Step 7: Rename folder
                rename_demo_app(requirement, level, context, success)
                
                print(f"Completed {requirement}/{level}/{context} - {'PASS' if success else 'FAIL'}")

if __name__ == "__main__":
    main()
