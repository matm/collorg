= how to grant an access
Just add a link between a function and a task. The users aving a role linked to the function will have access to all actions linked to the task. ex:

{{{
INSERT INTO "collorg.application".a_task_function (task, function, description) VALUES ( ( SELECT cog_oid FROM "collorg.application".task WHERE name = 'Articles'), (SELECT cog_oid FROM "collorg.actor".function where long_name = 'Directeur adjoint de département'), NULL);

}}}
