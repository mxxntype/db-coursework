-- A function for safely creating a ROLE, without causing exceptions.
CREATE OR REPLACE FUNCTION create_role_safe(rolename NAME, passwd VARCHAR) RETURNS TEXT AS
$$BEGIN
    EXECUTE format('CREATE ROLE %I WITH LOGIN PASSWORD %L', rolename, passwd);
    RETURN 'CREATE ROLE';
EXCEPTION
    WHEN duplicate_object THEN
        RETURN format('ROLE "%I" ALREADY EXISTS', rolename);
END; $$ LANGUAGE plpgsql;

-- Create the reader (regular user) role and grant it necessary permissions.
SELECT create_role_safe('reader', '12345');
GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;
GRANT INSERT ON ratings TO reader;

-- Create the author (admin user) role and grant it necessary permissions.
SELECT create_role_safe('author', '12345');
GRANT SELECT ON ALL TABLES IN SCHEMA public TO author;
GRANT INSERT ON ALL TABLES IN SCHEMA public TO author;
