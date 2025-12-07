-- Consolidated CREATE TABLE statements for demo-card-app

CREATE TABLE users (
    user_id INT PRIMARY KEY ,
    login_id VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL
);

CREATE TABLE card (
    card_id INT PRIMARY KEY,
    card_set CHAR(3),
    card_subset_id INT,
    card_name VARCHAR(100),
    color CHAR(1),
    card_type VARCHAR(50),
    subset_num INT,
    rarity CHAR(1),
    file_loc VARCHAR(100)
);

CREATE TABLE card_subset (
    card_subset_id INT PRIMARY KEY ,
    set_name VARCHAR(100),
    release_date DATE,
    total_cards INT
);

CREATE TABLE user_card (
    user_card_id INT PRIMARY KEY ,
    user_id INT,
    card_id INT,
    quantity INT
);

CREATE TABLE user_hist (
    user_hist_id SERIAL PRIMARY KEY,
    user_id INT,
    dt_tm TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    txt TEXT
);

CREATE TABLE goals (
    goal_id SERIAL PRIMARY KEY,
    user_id INT,
    goal_type VARCHAR(10),
    qty INT,
    create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE inventory (
    card_id INT PRIMARY KEY,
    price NUMERIC(10,2) NOT NULL,
    available_qty INT NOT NULL DEFAULT 0,
    FOREIGN KEY (card_id) REFERENCES card(card_id)
);

CREATE TABLE cart (
    user_id INT,
    card_id INT,
    quantity INT NOT NULL DEFAULT 1,
    price NUMERIC(10,2) NOT NULL,
    PRIMARY KEY (user_id, card_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (card_id) REFERENCES card(card_id)
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    subtotal NUMERIC(10,2) NOT NULL,
    tax_amount NUMERIC(10,2) NOT NULL,
    total_amount NUMERIC(10,2) NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT NOT NULL,
    card_id INT NOT NULL,
    card_name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2) NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (card_id) REFERENCES card(card_id)
);
