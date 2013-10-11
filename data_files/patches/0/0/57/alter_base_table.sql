alter table "collorg.core".base_table rename cog_presentation to cog_environment;
alter table "collorg.core".base_table alter column cog_environment set data type c_oid;
alter table "collorg.core".base_table add constraint base_table_cog_environment_fkey foreign key (cog_environment) references "collorg.core".oid_table(cog_oid);
update "collorg.web".topic set cog_environment = environment ;
