create table "collorg.web".a_rss_topic (
   rss c_oid,
       foreign key (rss) references "collorg.web".rss(key) on delete cascade,
   topic c_oid,
   foreign key (topic)
       references "collorg.web".topic(cog_oid) on delete cascade
);