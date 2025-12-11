# Demo Card AI Runner

A test harness for evaluating AI coding assistants (specifically Amazon Q) on a full-stack card collection application. The runner executes various coding tasks at different difficulty levels and context configurations, then validates results through automated testing.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Usage](#usage)
- [Configuration](#configuration)
- [Test Matrix](#test-matrix)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before getting started, ensure you have the following installed:

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.8+ | For running the test harness |
| Docker | 20.10+ | For containerized services |
| Docker Compose | 2.0+ | For orchestrating multi-container setup |
| Node.js | 18+ | For running the test suite |
| Amazon Q CLI | Latest | The AI assistant being evaluated |

### Verify Prerequisites

```bash
# Check Python version
python3 --version

# Check Docker
docker --version
docker compose version

# Check Node.js
node --version

# Check Amazon Q CLI
q --version
```

### Installing Amazon Q CLI

If you don't have Amazon Q CLI installed:

**macOS:**
```bash
brew install amazon-q
```

**Linux:**
```bash
# Download and install
curl -fsSL https://desktop-release.codewhisperer.us-east-1.amazonaws.com/latest/q-x86_64-linux.tar.gz -o q.tar.gz
tar -xzf q.tar.gz
./q/install.sh

# Or install to a specific location
./q/install.sh --install-dir /path/to/install --bin-dir /path/to/bin
```

**Windows:**
```bash
# Download installer from AWS
# https://desktop-release.codewhisperer.us-east-1.amazonaws.com/latest/q-x86_64-windows.msi
```

For more details, see the [Amazon Q Developer CLI documentation](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html).

---

## Installation

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd demo-card-ai-runner
```

### Step 2: Install Python Dependencies

```bash
pip install requests
```

### Step 3: Set Up the Demo Card App

Copy the demo-card-app source code to the expected location:

```bash
# Create the original app directory (this serves as the source for each test run)
cp -r /path/to/demo-card-app ../demo-card-app-orig
```

> **Important**: The runner expects `demo-card-app-orig` to exist in the parent directory (`/code/` by default). Each test run copies this to `demo-card-app`, runs the AI assistant, and then renames the folder with results.

### Step 4: Configure Paths (if needed)

Edit the configuration section in `ai-runner.py` if your paths differ from the defaults:

```python
# Configuration
Q_BIN_FOLDER = "/home/john/.local/bin/"   # Path to Amazon Q CLI
CODE_FOLDER = "/code/"                     # Parent folder for demo apps
DEMO_APP = os.path.join(CODE_FOLDER, "demo-card-app")
DEMO_APP_ORIG = os.path.join(CODE_FOLDER, "demo-card-app-orig")
RUNNER_FOLDER = "/code/demo-card-ai-runner"
```

---

## Environment Setup

### Amazon Q CLI Authentication

The AI runner uses Amazon Q CLI to execute coding tasks. Set up authentication:

```bash
# Required for SSO authentication
export Q_FAKE_IS_REMOTE=1

# Login to Amazon Q
q login
```

Follow the prompts to complete authentication.

### Docker Environment

The test harness uses Docker to run the full-stack application:

- **PostgreSQL**: Database for the card application
- **REST API**: Node.js/Express backend
- **Frontend**: Angular application
- **DB Setup**: Initialization container

Services are automatically started/stopped during test runs.

### Directory Structure

After setup, your directory structure should look like:

```
/code/
├── demo-card-ai-runner/     # This repository
│   ├── ai-runner.py         # Main test harness
│   ├── assets/              # Test assets and configurations
│   │   ├── db/              # Database scripts
│   │   ├── testing/         # Playwright test suite
│   │   ├── docker-compose.yml
│   │   └── *.md             # Context files for different C levels
│   └── results.csv          # Test results output
├── demo-card-app-orig/      # Original app (source for copies)
└── demo-card-app/           # Working copy (created during runs)
```

---

## Usage

### Basic Usage

Run all tests from the beginning:

```bash
python3 ai-runner.py
```

### Resume from a Specific Position

If a run is interrupted, resume from a specific test:

```bash
python3 ai-runner.py --start-from R3/L2/C5
```

Format: `R<requirement>/L<level>/C<context>`

### Usage Examples

#### Example 1: Full Test Run

```bash
# Ensure Amazon Q is authenticated
export Q_FAKE_IS_REMOTE=1
q login

# Run all tests
python3 ai-runner.py
```

#### Example 2: Resume After Interruption

```bash
# Check results.csv to see last completed test
tail -5 results.csv

# Resume from the next test
python3 ai-runner.py --start-from R5/L1/C1
```

#### Example 3: Run a Specific Requirement

Currently, running a single test requires modifying the source code or using `--start-from` and interrupting after completion.

### Understanding Output

During execution, you'll see:

```
Running R2/L1/C3...
Found docker-compose.yml, rebuilding services...
Waiting for database to be ready...
Database is ready
Completed R2/L1/C3 - PASS
```

Results are saved to:
- `results.csv` - CSV format: `Requirement,Level,Context,Success(0/1)`
- `demo-card-app-R2_L1_C3_1/LOG.txt` - Full execution log

---

## Configuration

### Test Matrix Explained

| Component | Values | Description |
|-----------|--------|-------------|
| **Requirements (R)** | R0-R7 | Different coding tasks (see below) |
| **Levels (L)** | L1, L2, L3 | Prompt specificity (L1=vague, L3=detailed) |
| **Contexts (C)** | C1-C9 | Amount of context provided to the AI |

### Requirements Overview

| ID | Task Description |
|----|------------------|
| R0 | Baseline test (no changes) |
| R1 | Update placeholder value (-1 to -2) |
| R2 | Implement real card count from database |
| R3 | Add inventory validation to cart |
| R4 | Implement state-based tax calculation |
| R5 | Add "Total Unique" goal type |
| R6 | Add "Total Above 4" goal type |
| R7 | Implement VIP badge feature |

### Context Levels

| Level | Included Assets |
|-------|-----------------|
| C1 | No additional context |
| C2 | CLAUDE_PERSONA.md |
| C3 | CLAUDE_CHECKLIST.md |
| C4 | C3 + PROJECT.md |
| C5 | C4 + CTAS.sql |
| C6 | C4 + DBConnect.md + db scripts + docker-compose |
| C7 | C4 + DBScripts.md + utility scripts + db + docker-compose |
| C8 | C7 + STARTSERVICE.md + start_service.py |
| C9 | C7 + TESTING.md + testing folder |

### Skip Logic

The runner automatically skips tests when a simpler configuration has already succeeded:
- If R2/L1/C3 passes, R2/L2/C3 and R2/L1/C5 are skipped (higher L or C not needed)

---

## Troubleshooting

### Common Issues

#### 1. Amazon Q CLI Not Found

**Error**: `q: command not found`

**Solution**: Ensure Amazon Q CLI is installed and in your PATH:

```bash
# Add to PATH (adjust path as needed)
export PATH="$PATH:/home/john/.local/bin"

# Or update Q_BIN_FOLDER in ai-runner.py
```

#### 2. Authentication Failed

**Error**: Amazon Q authentication issues

**Solution**:
```bash
# Set required environment variable
export Q_FAKE_IS_REMOTE=1

# Re-authenticate
q logout
q login
```

#### 3. Docker Services Won't Start

**Error**: Database or API containers fail to start

**Solution**:
```bash
# Clean up all containers and volumes
docker stop $(docker ps -q)
docker system prune -a --volumes

# Retry the test run
python3 ai-runner.py --start-from R2/L1/C1
```

#### 4. Database Not Ready

**Error**: `Warning: Database may not be ready`

**Solution**: The database may need more time. Check container logs:

```bash
docker logs postgres
docker logs db-setup
```

If issues persist, increase retry count in `wait_for_database()`.

#### 5. Test Timeout (20 minutes)

**Error**: `=== TIMEOUT: Process exceeded 20 minutes ===`

**Solution**: This indicates the AI took too long. The test is marked as failed and continues to the next iteration. Check the LOG.txt for details:

```bash
cat /code/demo-card-app-R*/LOG.txt | tail -100
```

#### 6. Missing demo-card-app-orig

**Error**: Source folder not found

**Solution**: Ensure the original app is copied to the correct location:

```bash
cp -r /path/to/demo-card-app /code/demo-card-app-orig
```

#### 7. Port Conflicts

**Error**: Port already in use (5432, 3001, 80)

**Solution**:
```bash
# Find and stop conflicting processes
lsof -i :5432
lsof -i :3001
lsof -i :80

# Or stop all Docker containers
docker stop $(docker ps -q)
```

### Viewing Results

```bash
# View all results
cat results.csv

# Count passes/failures
grep ",1$" results.csv | wc -l  # Passes
grep ",0$" results.csv | wc -l  # Failures

# View specific test log
cat /code/demo-card-app-R2_L1_C3_1/LOG.txt
```

### Getting Help

- Check `LOG.txt` in the renamed demo-card-app folders for detailed execution logs
- Review test output in the terminal for immediate feedback
- Examine `results.csv` to track progress and identify patterns

---

## Assets Reference

| File | Purpose |
|------|---------|
| `CLAUDE_PERSONA.md` | AI persona/behavior guidelines |
| `CLAUDE_CHECKLIST.md` | Task completion checklist |
| `PROJECT.md` | Project overview and architecture |
| `CTAS.sql` | Database schema reference |
| `DBConnect.md` | Database connection instructions |
| `DBScripts.md` | Database utility scripts documentation |
| `STARTSERVICE.md` | Service startup instructions |
| `TESTING.md` | Testing guidelines and commands |
| `run_query.py` | Database query utility |
| `schema_search.py` | Schema search utility |
| `start_service.py` | Service management utility |
