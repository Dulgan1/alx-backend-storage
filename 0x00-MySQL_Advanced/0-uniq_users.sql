-- SQL script creates new table users
-- with columns: id, email and name

CREATE TABLE IF NOT EXISTS users (
	`id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	`email` VARCHAR(255) NOT NULL UNIQUE,
	`name` VARCHAR(255)
)
