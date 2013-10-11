set search_path = "collorg.communication";
alter table a_tag_post drop constraint a_tag_post_post_fkey ;
alter table a_tag_post add constraint "a_tag_post_post_fkey" FOREIGN KEY (post) REFERENCES "collorg.core".oid_table(cog_oid);
