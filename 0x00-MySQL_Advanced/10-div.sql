-- Create a function that divides the first with the second
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    IF b = 0 THEN
        RETURN 0.0;
    ELSE
        RETURN a / b;
    END IF;
END $$
DELIMITER ;
