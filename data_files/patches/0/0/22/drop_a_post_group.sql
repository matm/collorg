DROP VIEW "collorg.communication.blog.view".by_post ;
DROP VIEW "collorg.communication.blog.view".by_user ;
drop table "collorg.communication.blog".a_post_group;
delete from "collorg.core".data_type where fqtn = 'collorg.communication.blog.a_post_group';
delete from "collorg.core".field where fqfn like 'collorg.communication.blog.a_post_group.%';
