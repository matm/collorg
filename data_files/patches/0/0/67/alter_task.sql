alter table "collorg.application".task add cog_from timestamp(0);
alter table "collorg.application".task add cog_to timestamp(0);
alter table "collorg.application".task inherit "collorg.time".duration;
