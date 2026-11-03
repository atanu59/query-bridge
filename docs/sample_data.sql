-- Sample shop database for Query Bridge.
-- Run it against an empty database, for example:
--   psql -U postgres -c "CREATE DATABASE shop_db;"
--   psql -U postgres -d shop_db -f docs/sample_data.sql

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    city        VARCHAR(50)
);

CREATE TABLE orders (
    order_id    SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    amount      NUMERIC(10,2),
    order_date  DATE
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    category   VARCHAR(50),
    price      NUMERIC(10,2)
);

CREATE TABLE order_items (
    item_id    SERIAL PRIMARY KEY,
    order_id   INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity   INT
);

INSERT INTO customers (name, city) VALUES
    ('Amit', 'Kolkata'),
    ('Riya', 'Agartala'),
    ('Sam', 'Delhi'),
    ('Neha', 'Mumbai'),
    ('Karan', 'Delhi'),
    ('Tara', 'Agartala'),
    ('Ishaan', 'Pune');

INSERT INTO orders (customer_id, amount, order_date) VALUES
    (1, 450.00, '2026-10-02'),
    (1, 800.50, '2026-10-15'),
    (2, 300.00, '2026-10-20'),
    (3, 1200.00, '2026-09-28'),
    (4, 150.00, '2026-10-05'),
    (4, 2200.00, '2026-10-28'),
    (5, 640.00, '2026-09-12'),
    (2, 90.00, '2026-08-30'),
    (6, 510.00, '2026-10-30');

INSERT INTO products (name, category, price) VALUES
    ('Notebook', 'Stationery', 60.00),
    ('Pen', 'Stationery', 10.00),
    ('Headphones', 'Electronics', 1500.00),
    ('Backpack', 'Accessories', 900.00),
    ('Desk Lamp', 'Home', 700.00);

INSERT INTO order_items (order_id, product_id, quantity) VALUES
    (1, 1, 3), (1, 2, 5), (2, 3, 1), (3, 4, 1), (4, 5, 1),
    (5, 2, 10), (6, 3, 1), (7, 1, 2), (8, 2, 4), (9, 5, 1);
