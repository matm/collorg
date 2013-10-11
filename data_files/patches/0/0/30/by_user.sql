SET search_path = "collorg.communication", "collorg.communication.blog",
    "collorg.event", "collorg.actor", "collorg.access";
CREATE VIEW "collorg.communication.blog.view".by_user AS
SELECT
post.cog_oid AS post_oid,
post.cog_creat_date AS post_creat_date,
event.begin_date AS event_begin_date,
post.cog_modif_date AS post_modif_date,
post.title AS post_title,
post.public AS public_post,
post.important AS important_post,
post.broadcast AS broadcast_post,
post.expiry_date AS expiry_date,
"user".cog_oid AS author_oid,
"user".first_name AS author_first_name,
"user".last_name AS author_last_name,
'[' || string_agg(distinct atp.tag, '][' order by atp.tag) || ']' AS tags,
data.cog_oid AS data_oid,
count(attachment) AS attachment
FROM
post
LEFT JOIN event ON
post.cog_oid = event.cog_oid
JOIN access ON
access.data = post.cog_oid
JOIN "collorg.access"."role" ON
role.access = access.cog_oid
JOIN function ON
role.function = function.cog_oid AND
function.long_name not like 'tmp%'
JOIN "user" ON
"user".cog_oid = access.user
LEFT JOIN a_post_data apd ON
post.cog_oid = apd.post
LEFT JOIN a_tag_post atp ON
post.cog_oid = atp.post
LEFT JOIN tag ON
atp.tag = tag.tag
LEFT JOIN "collorg.core".oid_table data ON
apd.data = data.cog_oid
LEFT JOIN "collorg.communication".attachment ON
attachment.data = post.cog_oid
GROUP BY
post.cog_oid, post.title, post."text", event.begin_date,
post.important, post.broadcast, post.expiry_date,
"user".cog_oid, "user".first_name, "user".last_name,
data.cog_oid
ORDER BY
event.begin_date, post.cog_creat_date
;
