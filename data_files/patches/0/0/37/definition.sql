create table "collorg.group".definition (
   "group" c_oid,
   constraint "group" foreign key("group")
   references "collorg.group"."group"(cog_oid),
   function c_oid,
   constraint function foreign key(function)
   references "collorg.actor".function(cog_oid),
   read boolean default 't',
   write boolean default 'f',
   admin boolean default 'f',
   moderator boolean default 'f',
   advertise boolean default 't',
   primary key("group", function)
);