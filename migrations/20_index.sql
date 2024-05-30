CREATE INDEX ON authors (phone);
CREATE INDEX ON ratings USING HASH (rated_at);
CREATE INDEX ON posts USING gin(to_tsvector('russian', text));

-- For the `B-Tree` index:
-- EXPLAIN SELECT * FROM authors WHERE phone = '7 (615) 255-2988';

-- For the `HASH` index:
-- EXPLAIN SELECT * FROM ratings WHERE rated_at = '2001-05-14 20:51:10';

-- For the `GIN` index:
-- EXPLAIN SELECT * FROM posts WHERE to_tsvector('russian', text) @@ to_tsquery('russian', 'слишком');
