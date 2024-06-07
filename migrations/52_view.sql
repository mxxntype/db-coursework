CREATE VIEW post_details AS
SELECT
    p.id AS post_id,
    p.title,
    p.text,
    p.author_id,
    a.name AS author_name,
    a.surname AS author_surname,
    a.middle_name AS author_middle_name,
    p.attachment_id,
    COALESCE(AVG(r.rate), 0) AS average_rating
FROM
    posts p
    JOIN authors a ON p.author_id = a.id
    LEFT JOIN ratings r ON p.id = r.post_id
GROUP BY
    p.id, p.title, p.text, p.author_id, a.name, a.surname, a.middle_name, p.attachment_id;

CREATE OR REPLACE FUNCTION insert_post_details()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO posts (title, text, author_id, attachment_id) 
    VALUES (NEW.title, NEW.text, NEW.author_id, NEW.attachment_id)
    RETURNING id INTO NEW.post_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER post_details_insert_trigger
INSTEAD OF INSERT ON post_details
FOR EACH ROW
EXECUTE FUNCTION insert_post_details();

CREATE OR REPLACE FUNCTION update_post_details()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE posts
    SET title = NEW.title, text = NEW.text, author_id = NEW.author_id, attachment_id = NEW.attachment_id
    WHERE id = NEW.post_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER post_details_update_trigger
INSTEAD OF UPDATE ON post_details
FOR EACH ROW
EXECUTE FUNCTION update_post_details();

CREATE OR REPLACE FUNCTION delete_post_details()
RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM posts WHERE id = OLD.post_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER post_details_delete_trigger
INSTEAD OF DELETE ON post_details
FOR EACH ROW
EXECUTE FUNCTION delete_post_details();
