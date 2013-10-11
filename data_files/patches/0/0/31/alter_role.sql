alter table "collorg.access".role drop constraint "function";
alter table "collorg.access".role add constraint "function" foreign key(function) references "collorg.actor".function(cog_oid);
alter table "collorg.access".role add "from" timestamp(0);
alter table "collorg.access".role add "to" timestamp(0);
alter table "collorg.access".role inherit "collorg.time".duration;
