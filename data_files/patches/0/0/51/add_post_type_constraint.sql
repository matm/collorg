alter table "collorg.web".topic add column post_type c_fqtn;
alter table "collorg.web".topic add constraint "post_type" foreign key(post_type) references "collorg.core".data_type(fqtn);
