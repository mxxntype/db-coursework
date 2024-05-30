-- A function with a subquery in the `SELECT` clause.
CREATE OR REPLACE FUNCTION top_rated_posts(post_limit INTEGER)
RETURNS TABLE (
    id             INTEGER,
    title          VARCHAR,
    text           TEXT,
    created_at     TIMESTAMP,
    average_rating NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.title,
        p.text,
        p.created_at,
        (
			SELECT AVG(r.rate) 
         	FROM ratings r 
         	WHERE r.post_id = p.id
		) AS average_rating
    FROM posts p ORDER BY average_rating DESC LIMIT post_limit;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM top_rated_posts(10);

-- A function with a subquery in the `WHERE` clause.
CREATE OR REPLACE FUNCTION get_posts_by_author_surname(a_surname VARCHAR)
RETURNS TABLE (
    id         INTEGER,
    title      VARCHAR,
    text       TEXT,
    created_at TIMESTAMP,
	author_id  BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.title,
        p.text,
        p.created_at,
		p.author_id
    FROM posts p
    WHERE p.author_id IN (SELECT a.id FROM authors a WHERE a.surname = a_surname);
END;
$$ LANGUAGE plpgsql;

SELECT * FROM get_posts_by_author_surname('Иванов');

-- A function with a subquery in the `FROM` clause.
CREATE OR REPLACE FUNCTION count_names_with_phone_like(pattern VARCHAR)
RETURNS TABLE (
    author_name VARCHAR,
    phone_count BIGINT
) AS
$$BEGIN
    RETURN QUERY
    SELECT name, count(*) as phones_starting_with_7
    FROM (SELECT * FROM authors WHERE phone LIKE pattern)
    GROUP BY name ORDER BY phones_starting_with_7 DESC;
END;
$$ LANGUAGE plpgsql;

SELECT * FROM count_names_with_phone_like('+7%');
