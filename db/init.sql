DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS delivery_agents;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    address TEXT
);

CREATE TABLE restaurants (
    id INTEGER PRIMARY KEY,
    name TEXT,
    cuisine TEXT
);

CREATE TABLE menu_items (
    id INTEGER PRIMARY KEY,
    restaurant_id INTEGER,
    name TEXT,
    price REAL,
    FOREIGN KEY(restaurant_id) REFERENCES restaurants(id)
);

CREATE TABLE delivery_agents (
    id INTEGER PRIMARY KEY,
    name TEXT,
    phone TEXT
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    restaurant_id INTEGER,
    delivery_agent_id INTEGER,
    total_amount REAL,
    order_date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(restaurant_id) REFERENCES restaurants(id),
    FOREIGN KEY(delivery_agent_id) REFERENCES delivery_agents(id)
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY,
    order_id INTEGER,
    menu_item_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(menu_item_id) REFERENCES menu_items(id)
);

-- Sample Data

INSERT INTO users VALUES (1, 'Alice', 'Pune');
INSERT INTO users VALUES (2, 'Bob', 'Mumbai');

INSERT INTO restaurants VALUES (1, 'Pizza Hub', 'Italian');
INSERT INTO restaurants VALUES (2, 'Spice Nation', 'Indian');

INSERT INTO menu_items VALUES (1, 1, 'Margherita Pizza', 350.0);
INSERT INTO menu_items VALUES (2, 2, 'Butter Chicken', 270.0);

INSERT INTO delivery_agents VALUES (1, 'Ravi', '9999988888');
INSERT INTO delivery_agents VALUES (2, 'Sunil', '9999977777');

INSERT INTO orders VALUES (1, 1, 1, 1, 700.0, '2024-07-01');
INSERT INTO orders VALUES (2, 2, 2, 2, 270.0, '2024-07-02');

INSERT INTO order_items VALUES (1, 1, 1, 2);
INSERT INTO order_items VALUES (2, 2, 2, 1);
