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
