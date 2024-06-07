CREATE MATERIALIZED VIEW author_activity_score AS
SELECT 
    authors.id AS author_id,
    authors.name || ' ' || authors.surname AS author_name,
    COUNT(posts.id) AS total_posts,
    COUNT(attachments.id) AS total_attachments,
    (COUNT(posts.id) + COUNT(attachments.id))::float / 2 AS total_activity_score
FROM 
    authors
LEFT JOIN 
    posts ON authors.id = posts.author_id
LEFT JOIN 
    attachments ON authors.id = attachments.author_id
GROUP BY 
    authors.id, authors.name, authors.surname;

REFRESH MATERIALIZED VIEW author_activity_score;
