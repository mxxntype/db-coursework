CREATE TABLE IF NOT EXISTS "authors" (
    "id" serial NOT NULL,
    "name" text,
    "surname" text,
    "middle_name" text,
    "phone" text,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "attachments" (
    "id" serial NOT NULL,
    "description" text,
    "data" text NOT NULL,
    "author_id" int,
    PRIMARY KEY("id"),
    FOREIGN KEY("author_id") REFERENCES "authors"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "posts" (
    "id" serial NOT NULL,
    "text" text,
    "title" text,
    "author_id" int,
    "attachment_id" int,
    PRIMARY KEY("id"),
    FOREIGN KEY("author_id") REFERENCES "authors"("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY("attachment_id") REFERENCES "attachments"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "ratings" (
    "id" serial NOT NULL,
    "post_id" int NOT NULL,
    "average" smallint,
    "count" int NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("post_id") REFERENCES "posts"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);
