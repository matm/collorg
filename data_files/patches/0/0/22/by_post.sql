SET search_path = "collorg.communication", "collorg.communication.blog",
    "collorg.actor", "collorg.group", "collorg.access";
CREATE VIEW "collorg.communication.blog.view".by_post AS
SELECT
post.cog_oid AS post_oid,
post.cog_creat_date AS post_creat_date,
post.cog_modif_date AS post_modif_date,
post.title AS post_title,
post.public AS public_post,
post.important AS important_post,
post.broadcast AS broadcast_post,
post.expiry_date AS expiry_date,
"user".cog_oid AS author_oid,
"user".first_name AS author_first_name,
"user".last_name AS author_last_name,
'[' || string_agg(distinct atp.tag, '][' order by atp.tag) || ']' as tags,
--'[' || string_agg(atp.tag, '][' order by atp.inst_tag desc, atp.order) || ']' AS tags,
--string_agg(atp.inst_tag::text, ' ' order by atp.inst_tag desc, atp.order) AS inst_tags,
data.cog_oid AS data_oid,
count(attachment) AS attachment
FROM
post
JOIN "group" ug ON
post.author_s_group = ug.cog_oid
JOIN "user" ON
ug.data = "user".cog_oid
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
post.cog_oid, post.title, post."text",
post.important, post.broadcast, post.expiry_date,
"user".cog_oid, "user".first_name, "user".last_name,
data.cog_oid
ORDER BY
post.cog_creat_date
;
