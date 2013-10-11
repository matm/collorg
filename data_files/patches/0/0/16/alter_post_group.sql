set search_path = "collorg.communication.blog";
alter table a_post_group drop constraint a_post_group_post_fkey;
alter table a_post_group add constraint a_post_group_post_fkey foreign key(post) references "collorg.core".oid_table(cog_oid);
