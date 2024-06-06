-- Normalize Phone Numbers on `UPDATE`.
CREATE OR REPLACE FUNCTION normalize_phone_number()
RETURNS TRIGGER AS $$
BEGIN
    NEW.phone := REGEXP_REPLACE(NEW.phone, '[^0-9]', '', 'g');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER normalize_phone_before_update
BEFORE UPDATE ON authors
FOR EACH ROW
EXECUTE FUNCTION normalize_phone_number();

-- Remove Orphaned Files on `DELETE`.
CREATE OR REPLACE FUNCTION remove_orphaned_files()
RETURNS TRIGGER AS $$
DECLARE
    file_hash VARCHAR;
BEGIN
    SELECT encode(digest(OLD.data, 'md5'), 'hex') INTO file_hash;
    PERFORM pg_notify('file_deleted', file_hash);
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER remove_files_after_delete
AFTER DELETE ON attachments
FOR EACH ROW
EXECUTE FUNCTION remove_orphaned_files();






-- Set Default Title on `INSERT`
CREATE OR REPLACE FUNCTION set_default_title()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.title IS NULL OR NEW.title = '' THEN
        NEW.title := 'Untitled Post';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_title_before_insert
BEFORE INSERT ON posts
FOR EACH ROW
EXECUTE FUNCTION set_default_title();

-- Validate Rating on `INSERT`
CREATE OR REPLACE FUNCTION validate_rating()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.rate < 1 OR NEW.rate > 5 THEN
        RAISE EXCEPTION 'Rating must be between 1 and 5';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_rating_before_insert
BEFORE INSERT ON ratings
FOR EACH ROW
EXECUTE FUNCTION validate_rating();
