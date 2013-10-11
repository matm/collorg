alter table "collorg.application".task_scheduler add column data c_oid references "collorg.core".oid_table(cog_oid);
alter table "collorg.application".task_scheduler add constraint "task_scheduler_year_data_key" unique("year", data);
