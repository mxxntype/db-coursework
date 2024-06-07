--
-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Debian 16.3-1.pgdg120+1)
-- Dumped by pg_dump version 16.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


--
-- Name: create_attachment(character varying, bytea, bigint); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.create_attachment(p_description character varying, p_data bytea, p_author_id bigint) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id BIGINT;
BEGIN
    INSERT INTO attachments (description, data, author_id)
    VALUES (p_description, p_data, p_author_id)
    RETURNING id INTO v_id;
    RETURN v_id;
END;
$$;


ALTER FUNCTION public.create_attachment(p_description character varying, p_data bytea, p_author_id bigint) OWNER TO admin;

--
-- Name: create_post(text, character varying, bigint, bigint); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.create_post(p_text text, p_title character varying, p_author_id bigint, p_attachment_id bigint DEFAULT NULL::bigint) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id BIGINT;
BEGIN
    INSERT INTO posts (text, title, author_id, attachment_id)
    VALUES (p_text, p_title, p_author_id, p_attachment_id)
    RETURNING id INTO v_id;
    RETURN v_id;
END;
$$;


ALTER FUNCTION public.create_post(p_text text, p_title character varying, p_author_id bigint, p_attachment_id bigint) OWNER TO admin;

--
-- Name: create_role_safe(name, character varying); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.create_role_safe(rolename name, passwd character varying) RETURNS text
    LANGUAGE plpgsql
    AS $$BEGIN
    EXECUTE format('CREATE ROLE %I WITH LOGIN PASSWORD %L', rolename, passwd);
    RETURN 'CREATE ROLE';
EXCEPTION
    WHEN duplicate_object THEN
        RETURN format('ROLE "%I" ALREADY EXISTS', rolename);
END; $$;


ALTER FUNCTION public.create_role_safe(rolename name, passwd character varying) OWNER TO admin;

--
-- Name: delete_attachment(bigint); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.delete_attachment(p_id bigint) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    DELETE FROM attachments WHERE id = p_id;
END;
$$;


ALTER FUNCTION public.delete_attachment(p_id bigint) OWNER TO admin;

--
-- Name: delete_author(bigint); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.delete_author(p_id bigint) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    DELETE FROM authors WHERE id = p_id;
END;
$$;


ALTER FUNCTION public.delete_author(p_id bigint) OWNER TO admin;

--
-- Name: delete_post(bigint); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.delete_post(p_id bigint) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    DELETE FROM posts WHERE id = p_id;
END;
$$;


ALTER FUNCTION public.delete_post(p_id bigint) OWNER TO admin;

--
-- Name: delete_post_details(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.delete_post_details() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    DELETE FROM posts WHERE id = OLD.post_id;
    RETURN OLD;
END;
$$;


ALTER FUNCTION public.delete_post_details() OWNER TO admin;

--
-- Name: delete_rating(bigint); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.delete_rating(p_id bigint) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    DELETE FROM ratings WHERE id = p_id;
END;
$$;


ALTER FUNCTION public.delete_rating(p_id bigint) OWNER TO admin;

--
-- Name: get_author_activity(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.get_author_activity() RETURNS TABLE(author_id integer, author_name text, total_posts bigint, total_attachments bigint, activity_level text)
    LANGUAGE plpgsql
    AS $$BEGIN
    RETURN QUERY
    SELECT 
        authors.id AS author_id,
        authors.name || ' ' || authors.surname AS author_name,
        COUNT(posts.id) AS total_posts,
        COUNT(attachments.id) AS total_attachments,
        CASE
            WHEN COUNT(posts.id) > 5 OR COUNT(attachments.id) > 3 THEN 'Высокий'
            WHEN COUNT(posts.id) > 2 OR COUNT(attachments.id) > 2 THEN 'Средний'
            ELSE 'Низкий'
        END AS activity_level
    FROM 
        authors
    LEFT JOIN 
        posts ON authors.id = posts.author_id
    LEFT JOIN 
        attachments ON authors.id = attachments.author_id
    GROUP BY 
        authors.id, authors.name, authors.surname
    ORDER BY 
        total_posts DESC, total_attachments DESC;
END; $$;


ALTER FUNCTION public.get_author_activity() OWNER TO admin;

--
-- Name: get_authors_with_high_rated_posts(smallint); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.get_authors_with_high_rated_posts(threshold smallint) RETURNS TABLE(author_id integer, name character varying, surname character varying, posts_with_high_rating bigint)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT 
        a.id AS author_id,
        a.name,
        a.surname,
        COUNT(p.id) AS posts_with_high_rating
    FROM 
        authors a
        INNER JOIN posts p ON a.id = p.author_id
    WHERE 
        EXISTS (
            SELECT 1
            FROM ratings r
            WHERE r.post_id = p.id
            AND r.rate > threshold
        )
    GROUP BY 
        a.id, a.name, a.surname
    ORDER BY 
        posts_with_high_rating DESC;
END;
$$;


ALTER FUNCTION public.get_authors_with_high_rated_posts(threshold smallint) OWNER TO admin;

--
-- Name: get_highest_rated_post_per_author(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.get_highest_rated_post_per_author() RETURNS TABLE(post_id integer, title character varying, text text, name character varying, surname character varying, created_at timestamp without time zone, rate smallint)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id AS post_id,
        p.title,
        p.text,
        a.name,
        a.surname,
        p.created_at,
        r.rate
    FROM 
        posts p
        INNER JOIN authors a ON p.author_id = a.id
        INNER JOIN ratings r ON p.id = r.post_id
    WHERE 
        r.rate = (
            SELECT MAX(r2.rate)
            FROM ratings r2
            INNER JOIN posts p2 ON r2.post_id = p2.id
            WHERE p2.author_id = p.author_id
        )
    ORDER BY 
        a.id, p.created_at DESC;
END;
$$;


ALTER FUNCTION public.get_highest_rated_post_per_author() OWNER TO admin;

--
-- Name: get_latest_rating_for_each_post(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.get_latest_rating_for_each_post() RETURNS TABLE(post_id bigint, latest_rating smallint, rated_at timestamp without time zone)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT r.post_id, r.rate, r.rated_at
    FROM ratings r
    WHERE r.rated_at = (
        SELECT MAX(r2.rated_at)
        FROM ratings r2
        WHERE r2.post_id = r.post_id
    );
END;
$$;


ALTER FUNCTION public.get_latest_rating_for_each_post() OWNER TO admin;

--
-- Name: get_post_count(bigint); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.get_post_count(aid bigint) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    result BIGINT;
BEGIN
    SELECT count(*) INTO result FROM posts WHERE author_id = aid;
    RETURN result;
END;
$$;


ALTER FUNCTION public.get_post_count(aid bigint) OWNER TO admin;

--
-- Name: get_posts_by_author_phone_numbers(character varying[]); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.get_posts_by_author_phone_numbers(phone_numbers character varying[]) RETURNS TABLE(post_id integer, post_title character varying, post_text text, author_name character varying, author_surname character varying)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.title, p.text, a.name, a.surname
    FROM posts p
    JOIN authors a ON p.author_id = a.id
    WHERE a.phone = ANY(phone_numbers);
END;
$$;


ALTER FUNCTION public.get_posts_by_author_phone_numbers(phone_numbers character varying[]) OWNER TO admin;

--
-- Name: get_posts_by_prolific_authors(integer); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.get_posts_by_prolific_authors(min_post_count integer) RETURNS TABLE(post_id integer, title character varying, text text)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id AS post_id,
        p.title,
        p.text
    FROM posts p
    WHERE 
        p.author_id IN (SELECT id FROM authors WHERE (SELECT COUNT(*) FROM posts WHERE author_id = authors.id) > min_post_count);
END;
$$;


ALTER FUNCTION public.get_posts_by_prolific_authors(min_post_count integer) OWNER TO admin;

--
-- Name: get_posts_with_author_count(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.get_posts_with_author_count() RETURNS TABLE(post_id integer, title character varying, text text, author_count bigint)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id AS post_id,
        p.title,
        p.text,
        (SELECT COUNT(*) FROM authors) AS author_count
    FROM posts p;
END;
$$;


ALTER FUNCTION public.get_posts_with_author_count() OWNER TO admin;

--
-- Name: get_posts_with_average_ratings(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.get_posts_with_average_ratings() RETURNS TABLE(post_id integer, title character varying, average_rating numeric)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT 
        sub.post_id,
        sub.title,
        sub.average_rating
    FROM 
        (SELECT 
             p.id AS post_id,
             p.title,
             COALESCE(AVG(r.rate), 0) AS average_rating
         FROM posts p
         LEFT JOIN ratings r ON p.id = r.post_id
         GROUP BY p.id, p.title) AS sub;
END;
$$;


ALTER FUNCTION public.get_posts_with_average_ratings() OWNER TO admin;

--
-- Name: get_posts_with_high_ratings(smallint[]); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.get_posts_with_high_ratings(min_ratings smallint[]) RETURNS TABLE(post_id integer, post_title character varying, post_text text, average_rate numeric)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.title, p.text, AVG(r.rate) AS average_rate
    FROM posts p
    JOIN ratings r ON p.id = r.post_id
    GROUP BY p.id, p.title, p.text
    HAVING AVG(r.rate) >= ALL(SELECT UNNEST(min_ratings));
END;
$$;


ALTER FUNCTION public.get_posts_with_high_ratings(min_ratings smallint[]) OWNER TO admin;

--
-- Name: insert_post_details(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.insert_post_details() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    INSERT INTO posts (title, text, author_id, attachment_id) 
    VALUES (NEW.title, NEW.text, NEW.author_id, NEW.attachment_id)
    RETURNING id INTO NEW.post_id;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.insert_post_details() OWNER TO admin;

--
-- Name: log_post_event(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.log_post_event() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
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
$$;


ALTER FUNCTION public.log_post_event() OWNER TO admin;

--
-- Name: normalize_phone_number(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.normalize_phone_number() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.phone := REGEXP_REPLACE(NEW.phone, '[^0-9]', '', 'g');
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.normalize_phone_number() OWNER TO admin;

--
-- Name: posts_with_avg_rate_above(numeric); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.posts_with_avg_rate_above(min_avg_rating numeric) RETURNS TABLE(author_id bigint, post_title character varying, average_rating numeric)
    LANGUAGE plpgsql
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
END; $$;


ALTER FUNCTION public.posts_with_avg_rate_above(min_avg_rating numeric) OWNER TO admin;

--
-- Name: rate_post(bigint, smallint); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.rate_post(p_post_id bigint, p_rate smallint) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id BIGINT;
BEGIN
    INSERT INTO ratings (post_id, rate)
    VALUES (p_post_id, p_rate)
    RETURNING id INTO v_id;
    RETURN v_id;
END;
$$;


ALTER FUNCTION public.rate_post(p_post_id bigint, p_rate smallint) OWNER TO admin;

--
-- Name: register_author(character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.register_author(p_name character varying, p_surname character varying, p_middle_name character varying, p_phone character varying DEFAULT NULL::character varying) RETURNS bigint
    LANGUAGE plpgsql
    AS $$
DECLARE
    v_id BIGINT;
BEGIN
    INSERT INTO authors (name, surname, middle_name, phone)
    VALUES (p_name, p_surname, p_middle_name, p_phone)
    RETURNING id INTO v_id;
    RETURN v_id;
END;
$$;


ALTER FUNCTION public.register_author(p_name character varying, p_surname character varying, p_middle_name character varying, p_phone character varying) OWNER TO admin;

--
-- Name: remove_orphaned_files(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.remove_orphaned_files() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    file_hash VARCHAR;
BEGIN
    SELECT encode(digest(OLD.data, 'md5'), 'hex') INTO file_hash;
    PERFORM pg_notify('file_deleted', file_hash);
    RETURN OLD;
END;
$$;


ALTER FUNCTION public.remove_orphaned_files() OWNER TO admin;

--
-- Name: sanitize_posts_and_authors(numeric, numeric); Type: PROCEDURE; Schema: public; Owner: admin
--

CREATE PROCEDURE public.sanitize_posts_and_authors(IN lower_threshold numeric, IN upper_threshold numeric)
    LANGUAGE plpgsql
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
                WHERE NOW() - created_at > INTERVAL '54 years'
            );
        
            COMMIT;
        END IF;
    END;
END;
$$;


ALTER PROCEDURE public.sanitize_posts_and_authors(IN lower_threshold numeric, IN upper_threshold numeric) OWNER TO admin;

--
-- Name: set_default_title(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.set_default_title() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.title IS NULL OR NEW.title = '' THEN
        NEW.title := 'Untitled Post';
    END IF;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.set_default_title() OWNER TO admin;

--
-- Name: update_attachment(bigint, character varying, bytea, bigint); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.update_attachment(p_id bigint, p_description character varying, p_data bytea, p_author_id bigint) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE attachments
    SET description = p_description,
        data = p_data,
        author_id = p_author_id
    WHERE id = p_id;
END;
$$;


ALTER FUNCTION public.update_attachment(p_id bigint, p_description character varying, p_data bytea, p_author_id bigint) OWNER TO admin;

--
-- Name: update_author(bigint, character varying, character varying, character varying, character varying); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.update_author(p_id bigint, p_name character varying, p_surname character varying, p_middle_name character varying, p_phone character varying DEFAULT NULL::character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE authors
    SET name = p_name, surname = p_surname, middle_name = p_middle_name, phone = p_phone
    WHERE id = p_id;
END;
$$;


ALTER FUNCTION public.update_author(p_id bigint, p_name character varying, p_surname character varying, p_middle_name character varying, p_phone character varying) OWNER TO admin;

--
-- Name: update_highly_rated_posts(numeric); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.update_highly_rated_posts(threshold numeric) RETURNS void
    LANGUAGE plpgsql
    AS $$
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
            SET title = '<i>[TOP]</i> ' || title
            WHERE id = rec.id;
        END IF;
    END LOOP;
    
    CLOSE cur;
END;
$$;


ALTER FUNCTION public.update_highly_rated_posts(threshold numeric) OWNER TO admin;

--
-- Name: update_post(bigint, text, character varying, bigint, bigint); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.update_post(p_id bigint, p_text text, p_title character varying, p_author_id bigint, p_attachment_id bigint DEFAULT NULL::bigint) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE posts
    SET text = p_text,
        title = p_title,
        author_id = p_author_id,
        attachment_id = p_attachment_id
    WHERE id = p_id;
END;
$$;


ALTER FUNCTION public.update_post(p_id bigint, p_text text, p_title character varying, p_author_id bigint, p_attachment_id bigint) OWNER TO admin;

--
-- Name: update_post_details(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.update_post_details() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE posts
    SET title = NEW.title, text = NEW.text, author_id = NEW.author_id, attachment_id = NEW.attachment_id
    WHERE id = NEW.post_id;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.update_post_details() OWNER TO admin;

--
-- Name: update_rating(bigint, bigint, smallint); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.update_rating(p_id bigint, p_post_id bigint, p_rate smallint) RETURNS void
    LANGUAGE plpgsql
    AS $$
BEGIN
    UPDATE ratings
    SET post_id = p_post_id,
        rate = p_rate
    WHERE id = p_id;
END;
$$;


ALTER FUNCTION public.update_rating(p_id bigint, p_post_id bigint, p_rate smallint) OWNER TO admin;

--
-- Name: validate_rating(); Type: FUNCTION; Schema: public; Owner: admin
--

CREATE FUNCTION public.validate_rating() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    IF NEW.rate < 1 OR NEW.rate > 5 THEN
        RAISE EXCEPTION 'Rating must be between 1 and 5';
    END IF;
    RETURN NEW;
END;
$$;


ALTER FUNCTION public.validate_rating() OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: attachments; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.attachments (
    id integer NOT NULL,
    description character varying,
    data bytea NOT NULL,
    author_id bigint NOT NULL
);


ALTER TABLE public.attachments OWNER TO admin;

--
-- Name: attachments_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.attachments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.attachments_id_seq OWNER TO admin;

--
-- Name: attachments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.attachments_id_seq OWNED BY public.attachments.id;


--
-- Name: authors; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.authors (
    id integer NOT NULL,
    name character varying NOT NULL,
    surname character varying NOT NULL,
    middle_name character varying NOT NULL,
    phone character varying
);


ALTER TABLE public.authors OWNER TO admin;

--
-- Name: posts; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.posts (
    id integer NOT NULL,
    text text NOT NULL,
    title character varying NOT NULL,
    author_id bigint NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    attachment_id bigint
);


ALTER TABLE public.posts OWNER TO admin;

--
-- Name: author_activity_score; Type: MATERIALIZED VIEW; Schema: public; Owner: admin
--

CREATE MATERIALIZED VIEW public.author_activity_score AS
 SELECT authors.id AS author_id,
    (((authors.name)::text || ' '::text) || (authors.surname)::text) AS author_name,
    count(posts.id) AS total_posts,
    count(attachments.id) AS total_attachments,
    (((count(posts.id) + count(attachments.id)))::double precision / (2)::double precision) AS total_activity_score
   FROM ((public.authors
     LEFT JOIN public.posts ON ((authors.id = posts.author_id)))
     LEFT JOIN public.attachments ON ((authors.id = attachments.author_id)))
  GROUP BY authors.id, authors.name, authors.surname
  WITH NO DATA;


ALTER MATERIALIZED VIEW public.author_activity_score OWNER TO admin;

--
-- Name: authors_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.authors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.authors_id_seq OWNER TO admin;

--
-- Name: authors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.authors_id_seq OWNED BY public.authors.id;


--
-- Name: ratings; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.ratings (
    id integer NOT NULL,
    post_id bigint NOT NULL,
    rate smallint NOT NULL,
    rated_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.ratings OWNER TO admin;

--
-- Name: post_details; Type: VIEW; Schema: public; Owner: admin
--

CREATE VIEW public.post_details AS
 SELECT p.id AS post_id,
    p.title,
    p.text,
    p.author_id,
    a.name AS author_name,
    a.surname AS author_surname,
    a.middle_name AS author_middle_name,
    p.attachment_id,
    COALESCE(avg(r.rate), (0)::numeric) AS average_rating
   FROM ((public.posts p
     JOIN public.authors a ON ((p.author_id = a.id)))
     LEFT JOIN public.ratings r ON ((p.id = r.post_id)))
  GROUP BY p.id, p.title, p.text, p.author_id, a.name, a.surname, a.middle_name, p.attachment_id;


ALTER VIEW public.post_details OWNER TO admin;

--
-- Name: post_logs; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.post_logs (
    id integer NOT NULL,
    text text NOT NULL,
    title character varying NOT NULL,
    author_id bigint NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    attachment_id bigint,
    event_type character varying(10) NOT NULL,
    event_time timestamp without time zone DEFAULT now(),
    description text
);


ALTER TABLE public.post_logs OWNER TO admin;

--
-- Name: post_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.post_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.post_logs_id_seq OWNER TO admin;

--
-- Name: post_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.post_logs_id_seq OWNED BY public.post_logs.id;


--
-- Name: posts_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.posts_id_seq OWNER TO admin;

--
-- Name: posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.posts_id_seq OWNED BY public.posts.id;


--
-- Name: ratings_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.ratings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ratings_id_seq OWNER TO admin;

--
-- Name: ratings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.ratings_id_seq OWNED BY public.ratings.id;


--
-- Name: attachments id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.attachments ALTER COLUMN id SET DEFAULT nextval('public.attachments_id_seq'::regclass);


--
-- Name: authors id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.authors ALTER COLUMN id SET DEFAULT nextval('public.authors_id_seq'::regclass);


--
-- Name: post_logs id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.post_logs ALTER COLUMN id SET DEFAULT nextval('public.post_logs_id_seq'::regclass);


--
-- Name: posts id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.posts ALTER COLUMN id SET DEFAULT nextval('public.posts_id_seq'::regclass);


--
-- Name: ratings id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.ratings ALTER COLUMN id SET DEFAULT nextval('public.ratings_id_seq'::regclass);


--
-- Name: attachments attachments_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.attachments
    ADD CONSTRAINT attachments_pkey PRIMARY KEY (id);


--
-- Name: authors authors_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.authors
    ADD CONSTRAINT authors_pkey PRIMARY KEY (id);


--
-- Name: post_logs post_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.post_logs
    ADD CONSTRAINT post_logs_pkey PRIMARY KEY (id);


--
-- Name: posts posts_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_pkey PRIMARY KEY (id);


--
-- Name: ratings ratings_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_pkey PRIMARY KEY (id);


--
-- Name: authors_phone_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX authors_phone_idx ON public.authors USING btree (phone);


--
-- Name: posts_to_tsvector_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX posts_to_tsvector_idx ON public.posts USING gin (to_tsvector('russian'::regconfig, text));


--
-- Name: ratings_rated_at_idx; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ratings_rated_at_idx ON public.ratings USING hash (rated_at);


--
-- Name: posts log_post_events_trigger; Type: TRIGGER; Schema: public; Owner: admin
--

CREATE TRIGGER log_post_events_trigger AFTER INSERT OR DELETE OR UPDATE ON public.posts FOR EACH ROW EXECUTE FUNCTION public.log_post_event();


--
-- Name: authors normalize_phone_before_update; Type: TRIGGER; Schema: public; Owner: admin
--

CREATE TRIGGER normalize_phone_before_update BEFORE UPDATE ON public.authors FOR EACH ROW EXECUTE FUNCTION public.normalize_phone_number();


--
-- Name: post_details post_details_delete_trigger; Type: TRIGGER; Schema: public; Owner: admin
--

CREATE TRIGGER post_details_delete_trigger INSTEAD OF DELETE ON public.post_details FOR EACH ROW EXECUTE FUNCTION public.delete_post_details();


--
-- Name: post_details post_details_insert_trigger; Type: TRIGGER; Schema: public; Owner: admin
--

CREATE TRIGGER post_details_insert_trigger INSTEAD OF INSERT ON public.post_details FOR EACH ROW EXECUTE FUNCTION public.insert_post_details();


--
-- Name: post_details post_details_update_trigger; Type: TRIGGER; Schema: public; Owner: admin
--

CREATE TRIGGER post_details_update_trigger INSTEAD OF UPDATE ON public.post_details FOR EACH ROW EXECUTE FUNCTION public.update_post_details();


--
-- Name: attachments remove_files_after_delete; Type: TRIGGER; Schema: public; Owner: admin
--

CREATE TRIGGER remove_files_after_delete AFTER DELETE ON public.attachments FOR EACH ROW EXECUTE FUNCTION public.remove_orphaned_files();


--
-- Name: posts set_title_before_insert; Type: TRIGGER; Schema: public; Owner: admin
--

CREATE TRIGGER set_title_before_insert BEFORE INSERT ON public.posts FOR EACH ROW EXECUTE FUNCTION public.set_default_title();


--
-- Name: ratings validate_rating_before_insert; Type: TRIGGER; Schema: public; Owner: admin
--

CREATE TRIGGER validate_rating_before_insert BEFORE INSERT ON public.ratings FOR EACH ROW EXECUTE FUNCTION public.validate_rating();


--
-- Name: attachments attachments_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.attachments
    ADD CONSTRAINT attachments_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.authors(id);


--
-- Name: post_logs post_logs_attachment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.post_logs
    ADD CONSTRAINT post_logs_attachment_id_fkey FOREIGN KEY (attachment_id) REFERENCES public.attachments(id);


--
-- Name: post_logs post_logs_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.post_logs
    ADD CONSTRAINT post_logs_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.authors(id);


--
-- Name: posts posts_attachment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_attachment_id_fkey FOREIGN KEY (attachment_id) REFERENCES public.attachments(id);


--
-- Name: posts posts_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.posts
    ADD CONSTRAINT posts_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.authors(id);


--
-- Name: ratings ratings_post_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.ratings
    ADD CONSTRAINT ratings_post_id_fkey FOREIGN KEY (post_id) REFERENCES public.posts(id) ON DELETE CASCADE;


--
-- Name: TABLE attachments; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT ON TABLE public.attachments TO reader;
GRANT SELECT ON TABLE public.attachments TO editor;


--
-- Name: SEQUENCE attachments_id_seq; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT,USAGE ON SEQUENCE public.attachments_id_seq TO reader;
GRANT SELECT,USAGE ON SEQUENCE public.attachments_id_seq TO editor;


--
-- Name: TABLE authors; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT ON TABLE public.authors TO reader;
GRANT SELECT ON TABLE public.authors TO editor;


--
-- Name: TABLE posts; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT ON TABLE public.posts TO reader;
GRANT SELECT,INSERT,UPDATE ON TABLE public.posts TO editor;


--
-- Name: TABLE author_activity_score; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT ON TABLE public.author_activity_score TO reader;
GRANT SELECT ON TABLE public.author_activity_score TO editor;


--
-- Name: SEQUENCE authors_id_seq; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT,USAGE ON SEQUENCE public.authors_id_seq TO reader;
GRANT SELECT,USAGE ON SEQUENCE public.authors_id_seq TO editor;


--
-- Name: TABLE ratings; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT,INSERT ON TABLE public.ratings TO reader;
GRANT SELECT,INSERT ON TABLE public.ratings TO editor;


--
-- Name: TABLE post_details; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT ON TABLE public.post_details TO reader;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE public.post_details TO editor;


--
-- Name: TABLE post_logs; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT ON TABLE public.post_logs TO reader;
GRANT SELECT,INSERT ON TABLE public.post_logs TO editor;


--
-- Name: SEQUENCE post_logs_id_seq; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT,USAGE ON SEQUENCE public.post_logs_id_seq TO reader;
GRANT SELECT,USAGE ON SEQUENCE public.post_logs_id_seq TO editor;


--
-- Name: SEQUENCE posts_id_seq; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT,USAGE ON SEQUENCE public.posts_id_seq TO reader;
GRANT SELECT,USAGE ON SEQUENCE public.posts_id_seq TO editor;


--
-- Name: SEQUENCE ratings_id_seq; Type: ACL; Schema: public; Owner: admin
--

GRANT SELECT,USAGE ON SEQUENCE public.ratings_id_seq TO reader;
GRANT SELECT,USAGE ON SEQUENCE public.ratings_id_seq TO editor;


--
-- PostgreSQL database dump complete
--
