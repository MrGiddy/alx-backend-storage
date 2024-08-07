-- Create a table `users` with `id`, `email`, `name` and `country` columns

CREATE TABLE IF NOT EXISTS users (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `email` VARCHAR(255) UNIQUE NOT NULL,
    `name` VARCHAR(255),
    `country` CHAR(2) NOT NULL DEFAULT 'US',
    CHECK ( `country` in ('US', 'CO', 'TN') )
);
