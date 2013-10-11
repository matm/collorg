alter table "collorg.access".access add column data c_oid ;
alter table "collorg.access".access add constraint "data"
  foreign key(data) references "collorg.core".oid_table(cog_oid);
