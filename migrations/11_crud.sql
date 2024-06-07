CREATE OR REPLACE FUNCTION
    register_author(p_name VARCHAR, p_surname VARCHAR, p_middle_name VARCHAR, p_phone VARCHAR DEFAULT NULL)
RETURNS BIGINT AS $$
DECLARE
    v_id BIGINT;
BEGIN
    INSERT INTO authors (name, surname, middle_name, phone)
    VALUES (p_name, p_surname, p_middle_name, p_phone)
    RETURNING id INTO v_id;
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION
    update_author(p_id BIGINT, p_name VARCHAR, p_surname VARCHAR, p_middle_name VARCHAR, p_phone VARCHAR DEFAULT NULL)
RETURNS VOID AS $$
BEGIN
    UPDATE authors
    SET name = p_name, surname = p_surname, middle_name = p_middle_name, phone = p_phone
    WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_author(p_id BIGINT) RETURNS VOID AS $$
BEGIN
    DELETE FROM authors WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION create_attachment(p_description VARCHAR, p_data BYTEA, p_author_id BIGINT) RETURNS BIGINT AS $$
DECLARE
    v_id BIGINT;
BEGIN
    INSERT INTO attachments (description, data, author_id)
    VALUES (p_description, p_data, p_author_id)
    RETURNING id INTO v_id;
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION
    update_attachment(p_id BIGINT, p_description VARCHAR, p_data BYTEA, p_author_id BIGINT)
RETURNS VOID AS $$
BEGIN
    UPDATE attachments
    SET description = p_description,
        data = p_data,
        author_id = p_author_id
    WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_attachment(p_id BIGINT) RETURNS VOID AS $$
BEGIN
    DELETE FROM attachments WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION
    create_post(p_text TEXT, p_title VARCHAR, p_author_id BIGINT, p_attachment_id BIGINT DEFAULT NULL)
RETURNS BIGINT AS $$
DECLARE
    v_id BIGINT;
BEGIN
    INSERT INTO posts (text, title, author_id, attachment_id)
    VALUES (p_text, p_title, p_author_id, p_attachment_id)
    RETURNING id INTO v_id;
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION
    update_post(p_id BIGINT, p_text TEXT, p_title VARCHAR, p_author_id BIGINT, p_attachment_id BIGINT DEFAULT NULL)
RETURNS VOID AS $$
BEGIN
    UPDATE posts
    SET text = p_text,
        title = p_title,
        author_id = p_author_id,
        attachment_id = p_attachment_id
    WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_post(p_id BIGINT) RETURNS VOID AS $$
BEGIN
    DELETE FROM posts WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION rate_post(p_post_id BIGINT, p_rate SMALLINT) RETURNS BIGINT AS $$
DECLARE
    v_id BIGINT;
BEGIN
    INSERT INTO ratings (post_id, rate)
    VALUES (p_post_id, p_rate)
    RETURNING id INTO v_id;
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_rating(p_id BIGINT, p_post_id BIGINT, p_rate SMALLINT) RETURNS VOID AS $$
BEGIN
    UPDATE ratings
    SET post_id = p_post_id,
        rate = p_rate
    WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION delete_rating(p_id BIGINT) RETURNS VOID AS $$
BEGIN
    DELETE FROM ratings WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;
