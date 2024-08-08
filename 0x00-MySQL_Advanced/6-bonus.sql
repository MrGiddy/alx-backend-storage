-- creates a stored procedure AddBonus that adds
-- a new correction for a student.
DELIMITER $$

CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score FLOAT)
BEGIN
    DECLARE project_id INT;

    -- Get the id if the project exists
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name;

    -- Add project_name to projects table if it is not there
    IF project_id IS NULL THEN
        INSERT INTO projects(name) VALUES(project_name);
        -- Get the project's id
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Add the project and the user's score to corrections table
    INSERT INTO corrections(user_id, project_id, score) VALUES (user_id, project_id, score);
END $$

DELIMITER ;
