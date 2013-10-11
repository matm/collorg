CREATE VIEW "collorg.access.view".task_function AS
SELECT
task.name AS task_name,
"function".name AS function_name
FROM
"collorg.application".task
JOIN "collorg.application".a_task_function atf ON
atf.task = task.cog_oid
JOIN "collorg.actor"."function" ON
atf."function" = "function".cog_oid;
