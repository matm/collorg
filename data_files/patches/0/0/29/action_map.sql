create view "collorg.application.view".action_map AS
SELECT
function.cog_oid AS function_oid,
function.name AS function_name,
goal.name AS goal_name,
task.cog_oid AS task_oid,
task.name AS task_name,
action.cog_oid,
action.name,
action.in_menu,
action.label,
data_type.fqtn
FROM "collorg.actor".function function
JOIN "collorg.application".a_task_function atf ON
atf.function = function.cog_oid
JOIN "collorg.application".task ON
atf.task = task.cog_oid
JOIN "collorg.application".a_action_task aat ON
aat.task = task.cog_oid
JOIN "collorg.application".action ON
aat.action = action.cog_oid
JOIN "collorg.core".data_type ON
action.data_type = data_type.fqtn
JOIN "collorg.application".a_task_goal atg ON
atg.task = task.cog_oid
JOIN "collorg.application".goal ON
atg.goal = goal.cog_oid;
