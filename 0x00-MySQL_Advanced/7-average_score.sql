-- Create procedure for average score of user
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
    DECLARE total INT DEFAULT 0;
    DECLARE counter INT DEFAULT 0;

    SELECT SUM(score)
        INTO total
        FROM corrections
        WHERE corrections.user_id = user_id;
    SELECT COUNT(*)
        INTO counter
        FROM corrections
        WHERE corrections.user_id = user_id;

    UPDATE users
        SET users.average_score = IF(counter = 0, 0, total / counter)
        WHERE users.id = user_id;
END $$
DELIMITER ;
