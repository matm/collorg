alter table "collorg.web".topic drop constraint topic_pkey;
alter table "collorg.web".topic add constraint topic_pkey primary key(environment, path_info);
alter table "collorg.web".topic drop column environment;