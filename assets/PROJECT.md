# Demo Card App - Project Documentation

## Overview
A full-stack trading card collection management application with e-commerce functionality. Users can track their card collections, set goals, purchase cards from a store, and manage their profile.

## Technology Stack

### Frontend
- **Framework**: Angular 20.3.0
- **Language**: TypeScript 5.9.2
- **Styling**: TailwindCSS 3.4.18
- **HTTP Client**: RxJS 7.8.0
- **Port**: 80 (mapped to 4200 internally)

### Backend
- **Framework**: Express 5.1.0
- **Language**: TypeScript 5.9.2
- **Runtime**: Node.js with ts-node
- **Database Client**: pg (node-postgres) 8.13.1
- **Port**: 3001

### Database
- **DBMS**: PostgreSQL 15
- **Database Name**: cardapp
- **Port**: 5432
- **Credentials**: postgres/password1!

### Infrastructure
- **Containerization**: Docker with docker-compose
- **Services**: postgres, db-setup, rest-api, frontend

## Project Structure

```
demo-card-app/
├── .amazonq/rules/          # AI assistant rules
│   └── CLAUDE.md            # Database update instructions
├── db/                      # Database setup and migrations
│   ├── 01 Create Tables.sql
│   ├── 02 Add Password Column.sql
│   ├── 03 Add Profile Fields.sql
│   ├── 04 Create Store Tables.sql
│   ├── 05 Create Order Tables.sql
│   ├── 10 Insert Test Users.sql
│   ├── 11 Intert Test Data - sets.sql
│   ├── 12 Insert Test Data - cards.sql
│   ├── 13 Insert Test Data - inventory.sql
│   ├── 99 Additional.sql    # For new database changes
│   ├── Dockerfile
│   └── setup.py             # Database initialization script
├── frontend/                # Angular application
│   ├── public/assets/       # Card images (meg/, wht/)
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/  # Reusable UI components
│   │   │   ├── guards/      # Route guards (auth.guard)
│   │   │   ├── pages/       # Page components
│   │   │   ├── services/    # API services
│   │   │   └── app.routes.ts
│   │   └── assets/          # Static assets
│   ├── Dockerfile
│   └── package.json
├── rest/                    # Express REST API
│   ├── src/
│   │   ├── app.ts           # Main application with all endpoints
│   │   └── database.ts      # PostgreSQL connection
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml       # Multi-container orchestration
```

## Database Schema

### Core Tables

#### users
- `user_id` INT PRIMARY KEY
- `login_id` VARCHAR(20) UNIQUE - Username for login
- `first_name` VARCHAR(50)
- `last_name` VARCHAR(50)
- `email` VARCHAR(100)
- `password` VARCHAR(100) - Plain text (default: 'password')
- `birthday` DATE
- `address_line1` VARCHAR(100)
- `address_line2` VARCHAR(100)
- `city` VARCHAR(50)
- `state` CHAR(2)
- `country` VARCHAR(3) - Default: 'USA'

#### card
- `card_id` INT PRIMARY KEY
- `card_set` CHAR(3) - Set identifier (e.g., 'meg', 'wht')
- `card_subset_id` INT - FK to card_subset
- `card_name` VARCHAR(100)
- `color` CHAR(1) - Card color code
- `card_type` VARCHAR(50)
- `subset_num` INT - Card number in set
- `rarity` CHAR(1) - Rarity code
- `file_loc` VARCHAR(100) - Image file path

#### card_subset
- `card_subset_id` INT PRIMARY KEY
- `set_name` VARCHAR(100)
- `release_date` DATE
- `total_cards` INT

#### user_card
- `user_card_id` INT PRIMARY KEY
- `user_id` INT - FK to users
- `card_id` INT - FK to card
- `quantity` INT - Number owned

#### user_hist
- `user_hist_id` SERIAL PRIMARY KEY
- `user_id` INT - FK to users
- `dt_tm` TIMESTAMP - Default: CURRENT_TIMESTAMP
- `txt` TEXT - Activity description

#### goals
- `goal_id` SERIAL PRIMARY KEY
- `user_id` INT - FK to users
- `goal_type` VARCHAR(10) - e.g., 'total'
- `qty` INT - Target quantity
- `create_date` TIMESTAMP - Default: CURRENT_TIMESTAMP

### Store Tables

#### inventory
- `card_id` INT PRIMARY KEY - FK to card
- `price` NUMERIC(10,2)
- `available_qty` INT - Default: 0

#### cart
- `user_id` INT - FK to users
- `card_id` INT - FK to card
- `quantity` INT - Default: 1
- `price` NUMERIC(10,2)
- PRIMARY KEY: (user_id, card_id)

#### orders
- `order_id` SERIAL PRIMARY KEY
- `user_id` INT - FK to users
- `subtotal` NUMERIC(10,2)
- `tax_amount` NUMERIC(10,2) - 5% tax rate
- `total_amount` NUMERIC(10,2)
- `order_date` TIMESTAMP - Default: CURRENT_TIMESTAMP

#### order_items
- `order_item_id` SERIAL PRIMARY KEY
- `order_id` INT - FK to orders
- `card_id` INT - FK to card
- `card_name` VARCHAR(100)
- `price` NUMERIC(10,2)
- `quantity` INT

## REST API Endpoints

### Authentication
- `POST /api/login` - Authenticate user
  - Body: `{ username, password }`
  - Returns: `0` (success) or `-1` (failure)

### User Management
- `GET /api/users` - Get all users (legacy)
- `GET /api/users/:id` - Get user by ID (legacy)
- `GET /api/user/:login_id` - Get user_id from login_id
- `GET /api/profile/:login_id` - Get user profile
- `POST /api/profile/:login_id` - Update user profile

### Collections
- `GET /api/collections` - Get all card sets
- `POST /api/cards` - Get cards with user collection data
  - Body: `{ card_set, login_id }`
  - Returns: Cards with quantity owned
- `PUT /api/cards/quantity` - Update card quantity in collection
  - Body: `{ card_id, user_id, quantity }`
  - Logs to user_hist

### Goals
- `GET /api/goals/:user_id` - Get all goals with progress
- `GET /api/goals-complete/:user_id` - Get count of completed goals
- `POST /api/goals` - Create new goal
  - Body: `{ user_id, goal_type, qty }`

### History
- `GET /api/user-hist/:user_id` - Get latest 10 history records

### Store
- `GET /api/store/cards` - Get all cards available in store
- `GET /api/cart/:user_id` - Get user's cart items
- `PUT /api/cart/update` - Update cart item quantity
  - Body: `{ user_id, card_id, quantity }`
- `POST /api/checkout` - Process checkout
  - Body: `{ user_id }`
  - Creates order, adds to collection, updates inventory, clears cart

## Frontend Routes

- `/login` - Login page (public)
- `/dashboard` - User dashboard (protected)
- `/goals` - Goals management (protected)
- `/collections` - View all card sets (protected)
- `/collections/:id` - View specific collection detail (protected)
- `/store` - Browse and purchase cards (protected)
- `/checkout` - Shopping cart and checkout (protected)
- `/profile` - User profile management (protected)

All routes except `/login` are protected by `authGuard`.

## Key Features

### Collection Management
- View card collections by set
- Track quantity owned for each card
- Add/remove cards from collection
- View collection history

### Goals System
- Create collection goals (e.g., "collect 100 total cards")
- Track progress with percent_complete calculation
- View completed goals count

### E-commerce
- Browse store inventory with prices
- Add cards to shopping cart
- Checkout process with 5% tax
- Order history tracking
- Automatic inventory updates
- Purchased cards added to collection

### User Profile
- Manage personal information
- Store birthday and address
- Profile persistence

## Development Notes

### Database Updates
- All new database changes should be added to `./db/99 Additional.sql`
- SQL files are executed in numerical order during db-setup
- Database is initialized on container startup

### Card Images
- Stored in `/frontend/public/assets/{set_name}/`
- Referenced via `file_loc` column in card table
- Placeholder images available for missing cards

### Authentication
- Simple username/password authentication
- No JWT or session management (basic implementation)
- Auth state managed in frontend service

### CORS
- API allows all origins (`*`)
- Suitable for development, should be restricted in production

## Running the Application

```bash
docker-compose up --build
```

Services will be available at:
- Frontend: http://localhost:80
- REST API: http://localhost:3001
- PostgreSQL: localhost:5432

## Test Data
- Test users inserted via `10 Insert Test Users.sql`
- Card sets: 'meg', 'wht' (from CSV files)
- Sample inventory with pricing
- Default password for all users: 'password'
