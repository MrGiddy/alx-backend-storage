-- creates a trigger that resets the attribute valid_email
-- only when the email has been changed.
DELIMITER $$

CREATE TRIGGER reset_valid_email_attribute
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    -- if the email has changed
    IF OLD.email != NEW.email THEN
        -- reset valid_email attribute
        SET NEW.valid_email = 0;
    END IF;
END$$

DELIMITER ;
