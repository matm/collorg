alter table "collorg.communication.blog".post no inherit "collorg.access".visibility;
drop table "collorg.access".visibility ;
alter table "collorg.communication.blog".post alter visibility set default 'private';
update "collorg.communication.blog".post set visibility = 'public';
drop view "collorg.communication.blog.view".by_post ;
