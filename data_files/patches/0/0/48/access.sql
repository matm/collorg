create view "collorg.access.view".access AS
SELECT
se.key AS session_key,
user_.cog_oid AS user_oid,
user_.pseudo AS user_pseudo,
user_.first_name AS user_first_name,
user_.last_name AS user_last_name,
function.cog_oid AS function_oid,
function.name AS function_name,
access.data AS data_oid,
oid_table.cog_fqtn AS fqtn,
goal.name AS goal_name,
task.cog_oid AS task_oid,
task.name AS task_name,
action.cog_oid,
action.cog_fqtn,
action.name,
action.in_menu,
action.in_header,
action.in_nav,
action.icon,
action.label
FROM
"collorg.web".session se
JOIN "collorg.actor"."user" user_ ON
se."user" = user_.cog_oid
JOIN "collorg.access".access access ON
access."user" = user_.cog_oid AND
access.begin_date <= now() AND
(access.end_date > now() OR access.end_date is NULL)
JOIN "collorg.core".oid_table ON
access.data = oid_table.cog_oid
JOIN "collorg.access".role role ON
access.cog_oid = role.access AND
role.cog_from <= now() AND
(role.cog_to > now() OR role.cog_to is NULL)
JOIN "collorg.actor".function function ON
role.function = function.cog_oid
JOIN "collorg.application".a_task_function atf ON
atf.function = function.cog_oid
JOIN "collorg.application".task ON
atf.task = task.cog_oid
JOIN "collorg.application".a_action_task aat ON
aat.task = task.cog_oid
JOIN "collorg.application".action ON
aat.action = action.cog_oid and
action.data_type = oid_table.cog_fqtn
left JOIN "collorg.application".a_task_goal atg ON
atg.task = task.cog_oid
left JOIN "collorg.application".goal ON
atg.goal = goal.cog_oid;
