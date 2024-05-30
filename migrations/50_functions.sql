-- A scalar function that counts the posts made by an author.
CREATE OR REPLACE FUNCTION get_post_count(aid BIGINT) RETURNS BIGINT AS $$
DECLARE
    result BIGINT;
BEGIN
    SELECT count(*) INTO result FROM posts WHERE author_id = aid;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- A vector function that calculates the total number of posts and attachments
-- per author, categorizing authors based on their activity level.
CREATE OR REPLACE FUNCTION get_author_activity()
RETURNS TABLE (
    author_id INT,
    author_name TEXT,
    total_posts BIGINT,
    total_attachments BIGINT,
    activity_level TEXT
)
AS $$BEGIN
    RETURN QUERY
    SELECT 
        authors.id AS author_id,
        authors.name || ' ' || authors.surname AS author_name,
        COUNT(posts.id) AS total_posts,
        COUNT(attachments.id) AS total_attachments,
        CASE
            WHEN COUNT(posts.id) > 5 OR COUNT(attachments.id) > 3 THEN 'Крайне активный'
            WHEN COUNT(posts.id) > 2 OR COUNT(attachments.id) > 2 THEN 'Активный'
            ELSE 'Малоактивный'
        END AS activity_level
    FROM 
        authors
    LEFT JOIN 
        posts ON authors.id = posts.author_id
    LEFT JOIN 
        attachments ON authors.id = attachments.author_id
    GROUP BY 
        authors.id, authors.name, authors.surname
    ORDER BY 
        total_posts DESC, total_attachments DESC;
END; $$ LANGUAGE plpgsql;
