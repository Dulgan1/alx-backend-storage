-- SQL script creates trigger to decrease no of items after an order
-- On items table

CREATE TRIGGER item_decrease BEFORE INSERT ON orders FOR EACH ROW UPDATE items
SET quantity = quantity - NEW.number WHERE name = NEW.item_name;
