CREATE OR REPLACE FUNCTION update_highly_rated_posts(threshold NUMERIC)
RETURNS VOID AS $$
DECLARE
    rec RECORD;
    cur CURSOR FOR 
    SELECT p.id, p.title, AVG(r.rate) AS average_rate
    FROM posts p
    JOIN ratings r ON p.id = r.post_id
    GROUP BY p.id, p.title;
BEGIN
    OPEN cur;
    LOOP
        FETCH cur INTO rec;
        EXIT WHEN NOT FOUND;
        
        IF rec.average_rate >= threshold THEN
            UPDATE posts
            SET title = '(Highly rated) ' || title
            WHERE id = rec.id;
        END IF;
    END LOOP;
    
    CLOSE cur;
END;
$$ LANGUAGE plpgsql;

-- SELECT update_highly_rated_posts(4.5);
