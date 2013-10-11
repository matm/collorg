create table "collorg.access".a_topic_function(
   function c_oid,
   constraint "function" foreign key("function")
   references "collorg.actor"."function"(cog_oid),
   topic c_oid,
   constraint "topic" foreign key(topic)
   references "collorg.web".topic(cog_oid),
   write boolean default 'f',
   moderate boolean default 'f',
   admin boolean default 'f',
   primary key("function", "topic")
) ;
