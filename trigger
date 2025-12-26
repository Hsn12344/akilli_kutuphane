DELIMITER $$

CREATE TRIGGER trg_create_fine_after_return
AFTER UPDATE ON borrow
FOR EACH ROW
BEGIN
    DECLARE days_late INT;
    DECLARE fine_amount DECIMAL(10,2);

    IF OLD.return_date IS NULL AND NEW.return_date IS NOT NULL THEN

        IF NEW.return_date > NEW.due_date THEN

            SET days_late = DATEDIFF(NEW.return_date, NEW.due_date);
            SET fine_amount = days_late * 10;

            IF NOT EXISTS (
                SELECT 1 FROM fine WHERE borrow_id = NEW.id
            ) THEN
                INSERT INTO fine (borrow_id, amount, is_paid)
                VALUES (NEW.id, fine_amount, 0);
            END IF;

        END IF;
    END IF;
END$$

DELIMITER ;



DELIMITER $$

CREATE TRIGGER trg_delete_fine_after_borrow_delete
AFTER DELETE ON borrow
FOR EACH ROW
BEGIN
    DELETE FROM fine WHERE borrow_id = OLD.id;
END$$

DELIMITER ;