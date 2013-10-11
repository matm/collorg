alter table "collorg.communication.blog".post drop constraint "post_author_s_group_fkey" ;
alter table "collorg.communication.blog".post alter COLUMN author_s_group drop not null ;
alter table "collorg.communication.blog".post add column author c_oid;
alter table "collorg.communication.blog".post add constraint "author" foreign key(author) references "collorg.actor"."user"(cog_oid);
