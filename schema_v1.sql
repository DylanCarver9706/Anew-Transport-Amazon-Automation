CREATE DATABASE IF NOT EXISTS amazon_orders;
USE amazon_orders;

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(255),
    order_number VARCHAR(255)
);

-- INSERT INTO orders (status, order_number) VALUES ('Completed', 'ABC123');
-- INSERT INTO orders (status, order_number) VALUES ('Pending', 'DEF456');