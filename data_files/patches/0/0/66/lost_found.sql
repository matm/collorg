set search_path to "collorg.core";
create view "collorg.core.view".lost_found as
select
oid_table.cog_oid,
oid_table.cog_fqtn,
base_table.cog_oid as bt_cog_oid
from
oid_table
left join base_table on
oid_table.cog_oid = base_table.cog_oid ;