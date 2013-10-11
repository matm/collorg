alter table "collorg.communication".a_tag_post add column data_type c_fqtn;
alter table "collorg.communication".a_tag_post add constraint a_tag_post_data_type_fkey FOREIGN KEY (data_type) REFERENCES "collorg.core".data_type(fqtn);
alter table "collorg.communication".a_tag_post add column status string;
