alter table "collorg.web".topic_graph drop constraint "parent";
alter table "collorg.web".topic_graph add constraint "parent" FOREIGN KEY (parent) REFERENCES "collorg.core".oid_table(cog_oid);
alter table "collorg.web".topic_graph add column link boolean default 'f';

