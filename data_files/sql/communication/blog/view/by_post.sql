SET search_path = "collorg.communication", "collorg.communication.blog",
    "collorg.event", "collorg.actor", "collorg.access", "collorg.web";
CREATE VIEW "collorg.communication.blog.view".by_post AS
SELECT
post.cog_oid,
post.cog_fqtn,
post.cog_creat_date AS post_creat_date,
case
    WHEN event.begin_date is NULL THEN post.cog_creat_date
    ELSE event.begin_date
END AS event_begin_date,
post.cog_modif_date AS post_modif_date,
post.title AS post_title,
post.introductory_paragraph,
post.public AS public_post,
post.visibility AS post_visibility,
post.important AS important_post,
post.broadcast AS broadcast_post,
post.expiry_date AS expiry_date,
topic.cog_oid AS author_topic_oid,
"user".cog_oid AS author_oid,
"user".first_name AS author_first_name,
"user".last_name AS author_last_name,
--'[' || string_agg(distinct atp.tag, '][' order by atp.tag) || ']' as tags,
--'[' || string_agg(atp.tag, '][' order by atp.inst_tag desc, atp.order) || ']' AS tags,
--string_agg(atp.inst_tag::text, ' ' order by atp.inst_tag desc, atp.order) AS inst_tags,
data.cog_oid AS data_oid,
count(distinct attachment.cog_oid) AS attachment,
count(distinct comment.cog_oid) as comment
FROM
post
LEFT JOIN event ON
post.cog_oid = event.cog_oid
LEFT JOIN "user" ON
post.author = "user".cog_oid
left join topic on
topic.cog_environment = "user".cog_oid
LEFT JOIN a_post_data apd ON
post.cog_oid = apd.post
--LEFT JOIN a_tag_post atp ON
--post.cog_oid = atp.post
--LEFT JOIN tag ON
--atp.tag = tag.tag
LEFT JOIN "collorg.core".oid_table data ON
apd.data = data.cog_oid
LEFT JOIN attachment ON
attachment.data = post.cog_oid
left join comment on
comment.data = post.cog_oid
GROUP BY
post.cog_oid, post.cog_fqtn, post.title,
post.introductory_paragraph, post."text", event.begin_date,
post.important, post.broadcast, post.expiry_date,
"user".cog_oid, "user".first_name, "user".last_name,
topic.cog_oid,
data.cog_oid
ORDER BY
event.begin_date, post.cog_creat_date
;
