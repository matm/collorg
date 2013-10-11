set search_path to
 "collorg.communication", "collorg.communication.blog", "collorg.actor";
create view "collorg.communication.view".comment as
select
post.cog_oid as post_oid,
comment.cog_oid as comment_oid,
comment.cog_creat_date as comment_creat_date,
comment.cog_modif_date as comment_modif_date,
comment.text as comment_text,
uc.cog_oid as user_comment_oid,
uc.first_name as user_comment_first_name,
uc.last_name as user_comment_last_name,
follow_up.cog_oid as follow_up_oid,
follow_up.cog_creat_date as follow_up_creat_date,
follow_up.cog_modif_date as follow_up_modif_date,
follow_up.text as follow_up_text,
uf.cog_oid as user_follow_up_oid,
uf.first_name as user_follow_up_first_name,
uf.last_name as user_follow_up_last_name
from
post
join comment on
comment.data = post.cog_oid
join "user" uc on
comment.author = uc.cog_oid
left join follow_up on
follow_up.comment = comment.cog_oid
left join "user" uf on
follow_up.author = uf.cog_oid;