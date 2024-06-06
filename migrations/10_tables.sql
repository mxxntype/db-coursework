CREATE TABLE IF NOT EXISTS authors (
    id          SERIAL  NOT NULL,
    name        VARCHAR NOT NULL,
    surname     VARCHAR NOT NULL,
    middle_name VARCHAR NOT NULL,
    phone       VARCHAR,
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS attachments (
    id          SERIAL   NOT NULL,
    description VARCHAR,
    data        BYTEA    NOT NULL,
    author_id   BIGINT   NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(author_id) REFERENCES authors(id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS posts (
    id            SERIAL    NOT NULL,
    text          TEXT      NOT NULL,
    title         VARCHAR   NOT NULL,
    author_id     BIGINT    NOT NULL,
    created_at    TIMESTAMP NOT NULL DEFAULT NOW(),
    attachment_id BIGINT,
    PRIMARY KEY(id),
    FOREIGN KEY(author_id) REFERENCES authors(id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    FOREIGN KEY(attachment_id) REFERENCES attachments(id)
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS ratings (
    id        SERIAL    NOT NULL,
    post_id   BIGINT    NOT NULL,
    rate      SMALLINT  NOT NULL,
    rated_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    PRIMARY KEY(id),
    FOREIGN KEY(post_id) REFERENCES posts(id)
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

CREATE EXTENSION IF NOT EXISTS pgcrypto;
