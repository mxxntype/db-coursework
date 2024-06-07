CREATE OR REPLACE FUNCTION get_posts_with_author_count()
RETURNS TABLE (
    post_id INTEGER,
    title VARCHAR,
    text TEXT,
    author_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id AS post_id,
        p.title,
        p.text,
        (SELECT COUNT(*) FROM authors) AS author_count
    FROM posts p;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_posts_by_prolific_authors(min_post_count INTEGER)
RETURNS TABLE (
    post_id INTEGER,
    title VARCHAR,
    text TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id AS post_id,
        p.title,
        p.text
    FROM posts p
    WHERE 
        p.author_id IN (SELECT id FROM authors WHERE (SELECT COUNT(*) FROM posts WHERE author_id = authors.id) > min_post_count);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_posts_with_average_ratings()
RETURNS TABLE (
    post_id INTEGER,
    title VARCHAR,
    average_rating NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        sub.post_id,
        sub.title,
        sub.average_rating
    FROM 
        (SELECT 
             p.id AS post_id,
             p.title,
             COALESCE(AVG(r.rate), 0) AS average_rating
         FROM posts p
         LEFT JOIN ratings r ON p.id = r.post_id
         GROUP BY p.id, p.title) AS sub;
END;
$$ LANGUAGE plpgsql;

-- SELECT * FROM get_posts_with_author_count();
-- SELECT * FROM get_posts_by_prolific_authors(13);
-- SELECT * FROM get_posts_with_average_ratings();
