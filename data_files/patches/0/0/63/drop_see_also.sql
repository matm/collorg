delete from "collorg.core".field where fqfn like 'collorg.communication.blog.see_also.%' ;
delete from "collorg.application".a_action_task where action in ( select cog_oid from "collorg.application".action where data_type = 'collorg.communication.blog.see_also' ) ;
delete from "collorg.application".action where data_type = 'collorg.communication.blog.see_also' ;
delete from "collorg.core".data_type where fqtn = 'collorg.communication.blog.see_also' ;
drop table "collorg.communication.blog".see_also;
