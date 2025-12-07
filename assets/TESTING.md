# Testing Guide

## Setup

Navigate to the testing folder and install dependencies:

```bash
cd testing
npm install
npx playwright install
```

## Running Tests

Run tests by providing test numbers as arguments:

```bash
node test-runner.js [test_numbers...]
```

### Examples

Single test:
```bash
node test-runner.js 100
```

Multiple tests:
```bash
node test-runner.js 100 200 300
```

## What the Tests Do

The test runner automatically:
1. Stops and rebuilds all Docker services
2. Waits for services to be ready
3. Runs the specified tests in order
4. Reports results

## Available Tests

- **100** - Login functionality
- **200** - Profile page (add/save/verify data)
- **300** - Add item to cart
- **310** - Shopping cart operations
- **350** - Verify checkout quantity is 12
- **351** - Verify checkout quantity is 10
- **360** - Verify total is $519.75
- **361** - Verify total is $433.13
- **362** - Verify total is $529.65
- **390** - Complete order
- **395** - Verify item unavailable
- **400** - Verify collection ownership (12 copies)
- **401** - Verify collection ownership (10 copies)
- **500** - Add quantities for 4 cards
- **600** - Create new goal (total)
- **601** - Verify goal completion 100%
- **650** - Create goal (total unique)
- **651** - Verify goal completion 50%
- **660** - Create goal (total above 4)
- **661** - Verify goal completion 50%
- **900** - Verify total cards is -1
- **901** - Verify total cards is -2
- **902** - Verify total cards is 16
- **950** - Verify star icon next to bob

## Prerequisites

- Docker and Docker Compose installed
- Node.js and npm installed
- Application services defined in docker-compose.yml
