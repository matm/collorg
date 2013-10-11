CREATE VIEW "collorg.access.view".by_function AS
SELECT
access.cog_oid,
access.pourcentage,
access.begin_date,
access.end_date,
access.data AS data_oid,
function.data_type AS data_fqtn,
user_.cog_oid AS user_oid,
user_.pseudo AS user_pseudo,
user_.first_name AS user_first_name,
user_.last_name AS user_last_name,
function.cog_oid AS function_oid,
function.name AS function_name,
function.long_name AS function_long_name,
function.advertise as function_advertise
FROM
"collorg.actor"."user" user_
JOIN "collorg.access".access access ON
access.user = user_.cog_oid AND
access.begin_date <= now() AND
(access.end_date is null or access.end_date > now())
left JOIN "collorg.access".role role ON
access.cog_oid = role.access and
(role.cog_from is null or role.cog_from <= now()) and
(role.cog_to is null or role.cog_to > now())
left JOIN "collorg.actor".function function ON
role.function = function.cog_oid
;
