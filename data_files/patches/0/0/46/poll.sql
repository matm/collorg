create table "collorg.communication".poll (
   shuffle int,
   post c_oid not null,
   foreign key (post)
      references "collorg.core".oid_table(cog_oid)
      on delete cascade,
   vote boolean -- false: -1, null: 0, true: +1
);
