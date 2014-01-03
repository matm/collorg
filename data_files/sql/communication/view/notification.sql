set search_path to "collorg.actor", "collorg.communication",
   "collorg.communication.blog", "collorg.access";
create view "collorg.communication.blog.view".notification as
select
"user".cog_oid as user_oid,
"user".email,
post.cog_oid as post_oid,
post.cog_fqtn,
post.title,
post.cog_creat_date,
post.cog_modif_date,
access.begin_date,
access.end_date,
last_visited.cog_modif_date as last_visited
from
"user"
join access on
access."user" = "user".cog_oid
join post on
access.data = post.cog_oid
left join last_visited on
"user".cog_oid = last_visited."user" and
post.cog_oid = last_visited.data;
