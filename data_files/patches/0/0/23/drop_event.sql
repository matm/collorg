drop schema "collorg.event" cascade ;
set search_path TO "collorg.application";
delete from a_action_task where action in (select cog_oid from action where data_type like 'collorg.event.%');
delete from action where data_type like 'collorg.event.%';
set search_path TO "collorg.core";
delete from field where fqfn like 'collorg.event.%' ;
delete from data_type where fqtn like 'collorg.event.%' ;
