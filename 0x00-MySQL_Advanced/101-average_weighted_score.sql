-- creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and stores the average weighted score for all students.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;

DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Update the average_scores column with the calculated weighted averages
    UPDATE users u
    JOIN (
        SELECT
            corrections.user_id,
            SUM(corrections.score * projects.weight) / SUM(projects.weight) AS weighted_avg
        FROM projects
        JOIN corrections
        ON projects.id = corrections.project_id
        GROUP BY corrections.user_id
    ) AS calculated_scores
    ON u.id = calculated_scores.user_id
    SET u.average_score = calculated_scores.weighted_avg;
END$$

DELIMITER ;
