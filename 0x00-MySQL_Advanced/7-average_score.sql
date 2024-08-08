-- creates a stored procedure ComputeAverageScoreForUser
-- that computes and stores the average score for a student
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
	DECLARE avg_score FLOAT;

	-- Compute the average score for the given user id
    SELECT AVG(score) INTO avg_score
    FROM corrections
    WHERE corrections.user_id = user_id;

	-- Update the average score for the user
    UPDATE users
    SET average_score = avg_score
    WHERE users.id = user_id;
END$$

DELIMITER ;
