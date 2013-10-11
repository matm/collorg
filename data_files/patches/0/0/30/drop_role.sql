drop view "collorg.group.view".membership;
drop table "collorg.group".a_group_role;
drop view "collorg.access.view".by_function;
alter table "collorg.access".access drop constraint "access_role_fkey";
drop view "collorg.access.view".access;
drop view "collorg.communication.blog.view".by_user;
alter table "collorg.access".access drop column "role";
drop table "collorg.organization".role_map;
drop table "collorg.actor".role;
