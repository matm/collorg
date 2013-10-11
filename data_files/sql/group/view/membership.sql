set search_path to "collorg.group", "collorg.access", "collorg.actor", "collorg.core";
create view "collorg.group.view".membership as
with user_access as (
     select
     access.cog_oid as access_oid,
     access.data as data_oid,
     access.begin_date as access_from,
     access.end_date as access_to,
     "user".cog_oid as user_oid,
     "user".first_name,
     "user".last_name,
     "user".email
     from
     access
     join "user" on
     access."user" = "user".cog_oid
     join oid_table on
     access.data = oid_table.cog_oid and
     oid_table.cog_fqtn = 'collorg.group.group'
), group_roles as (
   SELECT DISTINCT
   "user".cog_oid AS user_oid,
   "user".first_name,
   "user".last_name,
   "user".email,
   function.cog_oid as function_oid,
   function.name as function_name,
   function.long_name as function_long_name,
   function.advertise as function_advertise,
   role.cog_from as role_from,
   role.cog_to as role_to,
   "group".cog_oid as group_oid,
   "group".name as group_name,
   access.data as data_oid,
   function.data_type as data_fqtn,
   access.cog_oid as access_oid
   FROM
   "group"
   join definition on
   definition."group" = "group".cog_oid
   join function on
   definition.function = function.cog_oid
   join data_type on
   function.data_type = data_type.fqtn
   join oid_table on
   "group".data = oid_table.cog_oid
   join hierarchy on
   hierarchy.parent = oid_table.cog_oid
   join access on
   access.data = oid_table.cog_oid or
   access.data = hierarchy.child
   join "user" on
   access."user" = "user".cog_oid
   join role on
   role.access = access.cog_oid and
   role.function = function.cog_oid
)
select distinct
ua.user_oid,
ua.first_name,
ua.last_name,
ua.email,
ua.data_oid as group_oid,
ua.access_from,
ua.access_to,
gr.function_oid,
gr.function_name,
gr.function_long_name,
gr.function_advertise,
gr.data_oid,
gr.data_fqtn,
gr.group_name,
gr.role_from,
gr.role_to
from
user_access ua
left join group_roles gr on
ua.data_oid = gr.group_oid and
ua.user_oid = gr.user_oid;
