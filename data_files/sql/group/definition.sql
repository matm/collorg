create table "collorg.group".definition (
   "group" c_oid,
   constraint "group" foreign key("group")
   references "collorg.group"."group"(cog_oid),
   function c_oid,
   constraint function foreign key(function)
   references "collorg.actor".function(cog_oid),
   primary key("group", function)
);