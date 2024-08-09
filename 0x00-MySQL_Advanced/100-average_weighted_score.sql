-- creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    -- Declare local variables to use
    DECLARE weighted_sum FLOAT DEFAULT 0;
    DECLARE total_weight FLOAT DEFAULT 0;
    DECLARE weighted_average FLOAT DEFAULT 0;

    -- Calculate the weighted sum and total weight
    SELECT
        SUM(corrections.score * projects.weight), SUM(projects.weight)
    INTO weighted_sum, total_weight
    FROM projects
    JOIN corrections
    ON projects.id = corrections.project_id
    WHERE corrections.user_id = user_id;

    -- Calculate the user's weighted average
    IF total_weight > 0 THEN
        SET weighted_average = weighted_sum / total_weight;
    END IF;

    -- Update the user's average score
    UPDATE users
    SET average_score = weighted_average
    WHERE id = user_id;
END$$

DELIMITER ;
