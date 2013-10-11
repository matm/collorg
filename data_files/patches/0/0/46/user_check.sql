create table "collorg.communication".user_check (
   communication_object c_oid not null,
   foreign key (communication_object)
      references "collorg.core".oid_table(cog_oid)
      on delete cascade,
   "user" c_oid not null,
   foreign key ("user") references "collorg.actor"."user"(cog_oid)
      on delete cascade,
   date_checked timestamp(0),
   primary key(communication_object, "user")
);
