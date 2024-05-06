-- Create all necessary tables, in case they don't exist already.
CREATE TABLE IF NOT EXISTS "authors" (
    "id" serial NOT NULL,
    "name" TEXT,
    "surname" TEXT,
    "middle_name" TEXT,
    "phone" TEXT,
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS "attachments" (
    "id" serial NOT NULL,
    "description" TEXT,
    "data" text NOT NULL,
    "author_id" int,
    PRIMARY KEY("id"),
    FOREIGN KEY("author_id") REFERENCES "authors"("id") ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS "posts" (
    "id" serial NOT NULL,
    "text" TEXT,
    "title" TEXT,
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

-- A function for safely creating a ROLE, without causing exceptions.
--
-- SAFETY NOTE:
-- This function contains a race condition n the tiny time frame between looking
-- up the role and creating it. If a concurrent transaction creates the role in
-- between we get an exception after all. In most workloads, that will never
-- happen as creating roles is a rare operation carried out by an admin.
CREATE OR REPLACE FUNCTION create_role_safe(rolename NAME, passwd VARCHAR) RETURNS TEXT AS
$$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = rolename) THEN
        EXECUTE format('CREATE ROLE %I WITH LOGIN PASSWORD %L', rolename, passwd);
        RETURN 'CREATE ROLE';
    ELSE
        RETURN format('ROLE "%I" ALREADY EXISTS', rolename);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Create the reader (regular user) role and grant it necessary permissions.
SELECT create_role_safe('reader', '12345');
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
GRANT INSERT ON ratings TO reader;

-- Create the author (admin user) role and grant it necessary permissions.
SELECT create_role_safe('author', '12345');
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO author;
