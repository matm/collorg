CREATE TABLE "collorg.application".task_scheduler (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.application.task_scheduler'
      CHECK( cog_fqtn = 'collorg.application.task_scheduler' ),
   description WIKI,
   "year" int4,
   foreign key ("year") references "collorg.time"."year"(num),
   task c_oid not null,
   foreign key (task) references "collorg.application".task(cog_oid),
   PRIMARY KEY(cog_oid)
) INHERITS( "collorg.core".base_table, "collorg.time".duration ) ;
