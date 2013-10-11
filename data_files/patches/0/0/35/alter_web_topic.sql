alter table "collorg.web".topic add column site c_oid;
alter table "collorg.web".topic add constraint "site" foreign key(site) references "collorg.web".site(cog_oid);
