delete from "collorg.group".a_group_role ;

alter table "collorg.access".access drop constraint "access_pkey";
alter table "collorg.access".access alter COLUMN role drop not null ;

update "collorg.access".access set role = null ;
delete from "collorg.actor".role ;
delete from "collorg.access".access where data is null ;

alter table "collorg.access".access add constraint "access_pkey" primary key("user", data);
