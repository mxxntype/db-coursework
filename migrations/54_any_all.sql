CREATE OR REPLACE FUNCTION get_posts_by_author_phone_numbers(phone_numbers VARCHAR[])
RETURNS TABLE (
    post_id INTEGER,
    post_title VARCHAR,
    post_text TEXT,
    author_name VARCHAR,
    author_surname VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.title, p.text, a.name, a.surname
    FROM posts p
    JOIN authors a ON p.author_id = a.id
    WHERE a.phone = ANY(phone_numbers);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_posts_with_high_ratings(min_ratings SMALLINT[])
RETURNS TABLE (
    post_id INTEGER,
    post_title VARCHAR,
    post_text TEXT,
    average_rate NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.title, p.text, AVG(r.rate) AS average_rate
    FROM posts p
    JOIN ratings r ON p.id = r.post_id
    GROUP BY p.id, p.title, p.text
    HAVING AVG(r.rate) >= ALL(SELECT UNNEST(min_ratings));
END;
$$ LANGUAGE plpgsql;

-- SELECT * FROM get_posts_by_author_phone_numbers(ARRAY['86787060526', '+76750849371']);
-- SELECT * FROM get_posts_with_high_ratings(ARRAY[3::smallint, 4::smallint, 5::smallint]);
