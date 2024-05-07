-- Create all necessary tables, in case they don't exist already.
CREATE TABLE IF NOT EXISTS "authors" (
    "id" SERIAL NOT NULL,
    "name" TEXT,
    "surname" TEXT,
    "middle_name" TEXT,
    "phone" TEXT,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "attachments" (
    "id" SERIAL NOT NULL,
    "description" TEXT,
    "data" TEXT NOT NULL,
    "author_id" INT,
    PRIMARY KEY("id"),
    FOREIGN KEY("author_id") REFERENCES "authors"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "posts" (
    "id" SERIAL NOT NULL,
    "text" TEXT,
    "title" TEXT,
    "author_id" INT,
    "attachment_id" INT,
    PRIMARY KEY("id"),
    FOREIGN KEY("author_id") REFERENCES "authors"("id") ON UPDATE NO ACTION ON DELETE NO ACTION,
    FOREIGN KEY("attachment_id") REFERENCES "attachments"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "ratings" (
    "id" SERIAL NOT NULL,
    "post_id" INT NOT NULL,
    "average" SMALLINT,
    "count" INT NOT NULL,
    PRIMARY KEY("id"),
    FOREIGN KEY("post_id") REFERENCES "posts"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

-- A function for safely creating a ROLE, without causing exceptions.
CREATE OR REPLACE FUNCTION create_role_safe(rolename NAME, passwd VARCHAR) RETURNS TEXT AS
$$ BEGIN
    EXECUTE format('CREATE ROLE %I WITH LOGIN PASSWORD %L', rolename, passwd);
    RETURN 'CREATE ROLE';
EXCEPTION
    WHEN duplicate_object THEN
        RETURN format('ROLE "%I" ALREADY EXISTS', rolename);
END;
$$ LANGUAGE plpgsql;

-- Create the reader (regular user) role and grant it necessary permissions.
SELECT create_role_safe('reader', '12345');
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
GRANT INSERT ON ratings TO reader;

-- Create the author (admin user) role and grant it necessary permissions.
SELECT create_role_safe('author', '12345');
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO author;
