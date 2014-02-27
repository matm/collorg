SET search_path = "collorg.communication", "collorg.communication.blog",
    "collorg.core", "collorg.actor";
CREATE VIEW "collorg.communication.blog.view".children AS
SELECT
data.cog_oid as parent_oid,
post.cog_oid,
post.cog_fqtn,
post.cog_creat_date,
post.cog_modif_date,
post.title,
post.visibility,
post.introductory_paragraph,
post.public,
post.important,
post.broadcast,
post.expiry_date,
apd."order",
"user".cog_oid AS author_oid,
"user".first_name AS author_first_name,
"user".last_name AS author_last_name
FROM
post
LEFT JOIN "user" ON
post.author = "user".cog_oid
LEFT JOIN a_post_data apd ON
post.cog_oid = apd.post
LEFT JOIN oid_table data ON
apd.data = data.cog_oid
;
