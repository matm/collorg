DROP VIEW "collorg.access.view".by_function;
CREATE VIEW "collorg.access.view".by_function AS
SELECT
access.cog_oid,
access.pourcentage,
access.begin_date,
access.end_date,
user_.cog_oid AS user_oid,
user_.pseudo AS user_pseudo,
user_.first_name AS user_first_name,
user_.last_name AS user_last_name,
function.cog_oid AS function_oid,
function.name AS function_name,
function.long_name AS function_long_name,
--role.cog_oid AS role_oid,
role.data AS data_oid
FROM
"collorg.actor"."user" user_
JOIN "collorg.access".access access ON
access.user = user_.cog_oid AND
access.begin_date <= now() AND
(access.end_date is null or access.end_date > now())
JOIN "collorg.actor".role role ON
access.role = role.cog_oid
JOIN "collorg.actor".function function ON
role.function = function.cog_oid
;
