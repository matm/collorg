create table "collorg.communication".bookmark (
   post c_oid not null,
   foreign key (post) references "collorg.core".oid_table(cog_oid)
      on delete cascade,
   "user" c_oid not null,
   foreign key ("user") references "collorg.actor"."user"(cog_oid)
      on delete cascade,
   primary key(post, "user")
);
