-- SQL script creates stored procdure of creating trigger to validate email
-- on update on user email.

DELIMITER //
CREATE TRIGGER validate_email BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
    SET NEW.valid_email = 0;
    END IF;
END;
//
