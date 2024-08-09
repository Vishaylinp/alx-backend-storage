-- Create a procedure
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE PROCEDURE AddBonus (user_id INT, project_name VARCHAR(255), score FLOAT)
BEGIN
    DECLARE counter INT DEFAULT 0;
    DECLARE project_id INT DEFAULT 0;
    
    SELECT COUNT(id)
        INTO counter
        FROM projects
        WHERE name = project_name;
    IF counter = 0 THEN
        INSERT INTO projects(name)
            VALUES(project_name);
    END IF;
    SELECT id
        INTO project_id
        FROM projects
        WHERE name = project_name;
    INSERT INTO corrections(user_id, project_id, score)
        VALUES(user_Id, project_id, score);
END $$
DELIMITER ;
