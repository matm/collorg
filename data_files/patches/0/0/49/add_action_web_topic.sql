alter table "collorg.web".topic add column action c_oid;
alter table "collorg.web".topic add constraint "action" foreign key (action) references "collorg.application".action(cog_oid) on delete set null;
