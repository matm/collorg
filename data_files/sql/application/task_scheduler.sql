CREATE TABLE "collorg.application".task_scheduler (
   cog_oid C_OID UNIQUE NOT NULL
      REFERENCES "collorg.core".oid_table(cog_oid) INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.application.task_scheduler'
      CHECK( cog_fqtn = 'collorg.application.task_scheduler' ),
   description WIKI,
   task c_oid not null references "collorg.application".task(cog_oid),
   "year" int4 references "collorg.time"."year"(num),
   data c_oid references "collorg.core".oid_table(cog_oid),
   unique ("year", data),
   PRIMARY KEY(cog_oid)
) INHERITS( "collorg.core".base_table, "collorg.time".duration ) ;
