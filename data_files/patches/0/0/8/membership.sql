CREATE SCHEMA "collorg.group.view";
SET search_path = "collorg.group", "collorg.actor", "collorg.access";
CREATE VIEW "collorg.group.view".membership AS
SELECT
"user".cog_oid AS user_oid,
"user".first_name,
"user".last_name,
"user".email,
function.cog_oid as function_oid,
function.name as function_name,
function.advertise as function_advertise,
"group".cog_oid as group_oid,
"group".name as group_name,
role.data as data_oid
FROM
"user"
JOIN access ON
"user".cog_oid = access."user"
JOIN role ON
access.role = role.cog_oid
JOIN function ON
role.function = function.cog_oid
JOIN a_group_role ON
role.cog_oid = a_group_role.role
JOIN "group" ON
a_group_role.group = "group".cog_oid
;
