CREATE OR REPLACE PROCEDURE sanitize_posts_and_authors(
    IN lower_threshold NUMERIC,
    IN upper_threshold NUMERIC
)
AS $$
BEGIN
    BEGIN
        IF (lower_threshold > upper_threshold) THEN
            ROLLBACK;
        ELSE
            PERFORM update_highly_rated_posts(upper_threshold);
        
            DELETE FROM posts
            WHERE id IN (
                SELECT p.id
                FROM posts p
                JOIN ratings r ON p.id = r.post_id
                GROUP BY p.id
                HAVING AVG(r.rate) < lower_threshold
            );
        
            UPDATE authors
            SET phone = NULL
            WHERE id IN (
                SELECT DISTINCT author_id
                FROM posts
                WHERE created_at < NOW() - INTERVAL '1 year'
            );
        
            COMMIT;
        END IF;
    END;
END;
$$ LANGUAGE plpgsql;

-- CALL sanitize_posts_and_authors(2.0, 4.5);
