CREATE TABLE IF NOT EXISTS post_logs (
    id            SERIAL    NOT NULL,
    text          TEXT      NOT NULL,
    title         VARCHAR   NOT NULL,
    author_id     BIGINT    NOT NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    attachment_id BIGINT,
    event_type    VARCHAR(10) NOT NULL,
    event_time    TIMESTAMP DEFAULT now(),
    description   TEXT,
    PRIMARY KEY(id),
    FOREIGN KEY(author_id) REFERENCES authors(id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    FOREIGN KEY(attachment_id) REFERENCES attachments(id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE OR REPLACE FUNCTION log_post_event() RETURNS TRIGGER AS $$
BEGIN
    CASE TG_OP
        WHEN 'INSERT' THEN
            INSERT INTO
                post_logs(text, title, author_id, created_at, attachment_id, event_type, event_time, description)
            SELECT
                NEW.text,
                NEW.title,
                NEW.author_id,
                NEW.created_at,
                NEW.attachment_id,
                'INSERT',
                now(),
                'New post with title: ' || NEW.title;

        WHEN 'UPDATE' THEN
            INSERT INTO
                post_logs(text, title, author_id, created_at, attachment_id, event_type, event_time, description)
            SELECT
                NEW.text,
                NEW.title,
                NEW.author_id,
                NEW.created_at,
                NEW.attachment_id,
                'UPDATE',
                now(),
                'Post title updated from: ' || OLD.title || ' to: ' || NEW.title;

        WHEN 'DELETE' THEN
            INSERT INTO
                post_logs(text, title, author_id, created_at, attachment_id, event_type, event_time, description)
            SELECT
                OLD.text,
                OLD.title,
                OLD.author_id,
                OLD.created_at,
                OLD.attachment_id,
                'DELETE',
                now(),
                'Deleted post with title: ' || OLD.title;
    END CASE;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER log_post_events_trigger
    AFTER INSERT OR UPDATE OR DELETE ON posts
    FOR EACH ROW
    EXECUTE FUNCTION log_post_event();
