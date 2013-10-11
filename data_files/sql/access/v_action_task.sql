CREATE VIEW "collorg.access.view".action_task AS
SELECT
task.name AS task_name,
"action".name AS action_name,
data_type.fqtn AS data_fqtn
FROM
"collorg.application".task
JOIN "collorg.application".a_action_task aat ON
aat.task = task.cog_oid
JOIN "collorg.application"."action" ON
aat."action" = "action".cog_oid
JOIN "collorg.core".data_type ON
"action".data_type = data_type.fqtn;
