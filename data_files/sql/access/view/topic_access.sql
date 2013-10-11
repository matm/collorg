set search_path to "collorg.access", "collorg.actor", "collorg.core", "collorg.web";
create view "collorg.access.view".topic_access as
select distinct
"user".cog_oid as user_oid,
topic.cog_oid as topic_oid,
access.begin_date as access_from,
access.end_date as access_to,
function.cog_oid as function_oid,
atf.write,
atf.moderate,
atf.admin,
topic.visibility as topic_visibility
from
topic
join a_topic_function atf on
topic.cog_oid = atf.topic
join function on
atf.function = function.cog_oid
join role on
function.cog_oid = role.function
join access on
role.access = access.cog_oid
join "user" on
"user".cog_oid = access."user";