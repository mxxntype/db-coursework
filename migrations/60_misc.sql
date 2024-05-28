
-- A multi-table view for updating a post's title and text based on an ID.
CREATE VIEW post_updates AS
SELECT id, title, text
FROM posts;

CREATE OR REPLACE FUNCTION update_post()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE posts SET title = NEW.title, text = NEW.text WHERE id = NEW.id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER post_update_trigger
INSTEAD OF UPDATE ON post_updates
FOR EACH ROW
EXECUTE FUNCTION update_post();

-- Create a materialized view for getting authors' activity scores.
CREATE MATERIALIZED VIEW author_activity_score AS
SELECT 
    authors.id AS author_id,
    authors.name || ' ' || authors.surname AS author_name,
    COUNT(posts.id) AS total_posts,
    COUNT(attachments.id) AS total_attachments,
    (COUNT(posts.id) + COUNT(attachments.id))::float / 2 AS total_activity_score
FROM 
    authors
LEFT JOIN 
    posts ON authors.id = posts.author_id
LEFT JOIN 
    attachments ON authors.id = attachments.author_id
GROUP BY 
    authors.id, authors.name, authors.surname;

REFRESH MATERIALIZED VIEW author_activity_score;

-- A multi-table query that groups records, uses aggregate functions, includes
-- a parameter in the HAVING clause to view the average rating of each post.
CREATE OR REPLACE FUNCTION posts_with_avg_rate_above(min_avg_rating NUMERIC)
RETURNS TABLE (
    author_id BIGINT,
    post_title VARCHAR,
    average_rating NUMERIC
)
AS $$BEGIN
    RETURN QUERY
    SELECT 
        posts.author_id,
        posts.title,
        AVG(ratings.rate) AS average_rating
    FROM 
        posts
    JOIN 
        ratings ON posts.id = ratings.post_id
    GROUP BY 
        posts.author_id, posts.title
    HAVING 
        AVG(ratings.rate) > min_avg_rating;
END; $$ LANGUAGE plpgsql;

-- Get all posts that are written by any of the authors provided.
CREATE OR REPLACE FUNCTION get_posts_by_any_authors(author_ids BIGINT[])
RETURNS TABLE (
    post_title VARCHAR,
    author_id BIGINT
)
AS $$BEGIN
    RETURN QUERY
    SELECT 
        posts.title,
        posts.author_id
    FROM 
        posts
    WHERE 
        posts.author_id = ANY(author_ids);
END; $$ LANGUAGE plpgsql;

-- Get all posts that are written by all of the authors provided.
-- If an array has more than 1 element, no posts will ever be returned.
CREATE OR REPLACE FUNCTION get_posts_by_all_authors(author_ids BIGINT[])
RETURNS TABLE (
    post_title VARCHAR,
    author_id BIGINT
)
AS $$BEGIN
    RETURN QUERY
    SELECT 
        posts.title,
        posts.author_id
    FROM 
        posts
    WHERE 
        posts.author_id = ALL(author_ids);
END; $$ LANGUAGE plpgsql;
