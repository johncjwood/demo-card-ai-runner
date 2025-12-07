import os
import shutil
import subprocess
import sys

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
        "L2": "On the dashboard page, the default behavior is to display -1 as the total cards. \nUpdate it to be -2.",
        "L3": ""  # To be provided
    },
    "R2": {"L1": "", "L2": "", "L3": ""},
    "R3": {"L1": "", "L2": "", "L3": ""},
    "R4": {"L1": "", "L2": "", "L3": ""},
    "R5": {"L1": "", "L2": "", "L3": ""},
    "R6": {"L1": "", "L2": "", "L3": ""},
    "R7": {"L1": "", "L2": "", "L3": ""}
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
CONTEXTS = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12"]

def copy_demo_app():
    """Step 1: Copy demo-card-app-orig to demo-card-app"""
    if os.path.exists(DEMO_APP):
        shutil.rmtree(DEMO_APP)
    if os.path.exists(DEMO_APP_ORIG):
        shutil.copytree(DEMO_APP_ORIG, DEMO_APP)

def copy_context(context):
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

def run_amazonq(prompt):
    """Step 3 & 4: Run AmazonQ CLI with prompt, log output"""
    log_file = os.path.join(DEMO_APP, "LOG.txt")
    
    # AmazonQ CLI command
    q_cmd = os.path.join(Q_BIN_FOLDER, "q")
    cmd = [q_cmd, "chat", "--trust-all-tools", "--no-interactive", "--prompt", prompt]
    
    # Inherit environment and add Q_FAKE_IS_REMOTE if needed
    env = os.environ.copy()
    env["Q_FAKE_IS_REMOTE"] = "1"
    
    with open(log_file, "w") as f:
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
    
    # Check if all tests succeeded
    return result.returncode == 0 and "failed" not in result.stdout.lower()

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
    context_order = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11", "C12"]
    
    current_level_idx = level_order.index(level)
    current_context_idx = context_order.index(context)
    
    # Check smaller L levels with same context
    for i in range(current_level_idx):
        if results.get((requirement, level_order[i], context)) == 1:
            return True
    
    # Check smaller C levels with same L
    for i in range(current_context_idx):
        if results.get((requirement, level, context_order[i])) == 1:
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
                copy_context(context)
                
                # Step 3 & 4: Run AmazonQ
                run_amazonq(prompt)
                
                # Step 5a: Copy test assets
                copy_test_assets()
                
                # Step 5b: Run tests
                success = run_tests(requirement)
                
                # Step 6: Append results
                append_results(requirement, level, context, success)
                
                # Step 7: Rename folder
                rename_demo_app(requirement, level, context, success)
                
                print(f"Completed {requirement}/{level}/{context} - {'PASS' if success else 'FAIL'}")

if __name__ == "__main__":
    main()
