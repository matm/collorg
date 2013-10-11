DROP TABLE "collorg.application".a_task_role;
DELETE FROM "collorg.core".field WHERE fqfn like 'collorg.application.a_task_role.%' ;
DELETE FROM "collorg.core".data_type WHERE fqtn = 'collorg.application.a_task_role' ;
DELETE FROM "collorg.application".a_action_task WHERE  action = (
   SELECT cog_oid FROM "collorg.application".action WHERE label = 'User''s tasks list' );
DELETE FROM "collorg.application".action WHERE label = 'User''s tasks list';
DELETE from "collorg.core".oid_table where cog_oid not in (select cog_oid from "collorg.core".base_table ) ;
