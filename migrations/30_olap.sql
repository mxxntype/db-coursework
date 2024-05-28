-- An OLAP table.
CREATE TABLE post_logs (LIKE posts INCLUDING ALL);
ALTER TABLE post_logs
    ADD COLUMN event_type VARCHAR(10) NOT NULL,
    ADD COLUMN event_time TIMESTAMP DEFAULT now(),
    ADD COLUMN description TEXT;

-- A procedure for logging post events in the OLAP table above.
CREATE OR REPLACE FUNCTION log_post_event() RETURNS TRIGGER AS $$
BEGIN
    CASE TG_OP
        WHEN 'INSERT' THEN
            INSERT INTO post_logs SELECT NEW.*, 'INSERT', now(), 'New post with title: ' || NEW.title;
        WHEN 'UPDATE' THEN
            INSERT INTO post_logs SELECT NEW.*, 'UPDATE', now(), 'Post title updated from: ' || OLD.title || ' to: ' || NEW.title;
        WHEN 'DELETE' THEN
            INSERT INTO post_logs SELECT OLD.*, 'DELETE', now(), 'Deleted post with title: ' || OLD.title;
    END CASE;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- A OLAP-logging trigger for the `posts` table.
CREATE TRIGGER log_post_events_trigger
    AFTER INSERT OR UPDATE OR DELETE ON posts
    FOR EACH ROW
    EXECUTE FUNCTION log_post_event();
