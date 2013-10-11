alter table "collorg.web".page add environment c_oid;
alter table "collorg.web".page add constraint "environment" foreign key(environment) references "collorg.core".oid_table(cog_oid);
alter table "collorg.web".page add data_type c_oid;
alter table "collorg.web".page add constraint "data_type" foreign key(data_type) references "collorg.core".data_type(fqtn);
