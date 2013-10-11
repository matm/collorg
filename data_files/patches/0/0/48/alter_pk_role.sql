alter table "collorg.access".role alter COLUMN cog_from set DEFAULT ('now'::text)::timestamp(0) with time zone;
update "collorg.access".role set cog_from = now();
alter table "collorg.access".role drop constraint "role_pkey";
alter table "collorg.access".role add constraint "role_pkey" primary key(access, function, cog_from);
