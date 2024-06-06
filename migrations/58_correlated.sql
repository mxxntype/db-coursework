CREATE OR REPLACE FUNCTION get_latest_rating_for_each_post()
RETURNS TABLE(post_id BIGINT, latest_rating SMALLINT, rated_at TIMESTAMP) AS $$
BEGIN
    RETURN QUERY
    SELECT r.post_id, r.rate, r.rated_at
    FROM ratings r
    WHERE r.rated_at = (
        SELECT MAX(r2.rated_at)
        FROM ratings r2
        WHERE r2.post_id = r.post_id
    );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_highest_rated_post_per_author()
RETURNS TABLE(
    post_id INTEGER,
    title VARCHAR,
    text TEXT,
    name VARCHAR,
    surname VARCHAR,
    created_at TIMESTAMP,
    rate SMALLINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id AS post_id,
        p.title,
        p.text,
        a.name,
        a.surname,
        p.created_at,
        r.rate
    FROM 
        posts p
        INNER JOIN authors a ON p.author_id = a.id
        INNER JOIN ratings r ON p.id = r.post_id
    WHERE 
        r.rate = (
            SELECT MAX(r2.rate)
            FROM ratings r2
            INNER JOIN posts p2 ON r2.post_id = p2.id
            WHERE p2.author_id = p.author_id
        )
    ORDER BY 
        a.id, p.created_at DESC;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_authors_with_high_rated_posts(threshold SMALLINT)
RETURNS TABLE(
    author_id INTEGER,
    name VARCHAR,
    surname VARCHAR,
    posts_with_high_rating BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.id AS author_id,
        a.name,
        a.surname,
        COUNT(p.id) AS posts_with_high_rating
    FROM 
        authors a
        INNER JOIN posts p ON a.id = p.author_id
    WHERE 
        EXISTS (
            SELECT 1
            FROM ratings r
            WHERE r.post_id = p.id
            AND r.rate > threshold
        )
    GROUP BY 
        a.id, a.name, a.surname
    ORDER BY 
        posts_with_high_rating DESC;
END;
$$ LANGUAGE plpgsql;
