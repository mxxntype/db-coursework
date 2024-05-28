CREATE INDEX ON authors (phone);
-- EXPLAIN SELECT * FROM authors WHERE phone = '7 (615) 255-2988';

CREATE INDEX ON ratings USING HASH (rated_at);
-- EXPLAIN SELECT * FROM ratings WHERE rated_at = '2001-05-14 20:51:10';

CREATE INDEX ON posts USING BRIN (created_at);
-- TODO
