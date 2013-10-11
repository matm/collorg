CREATE TABLE "collorg.planning".task_schedule (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.planning.task_schedule'
      CHECK( cog_fqtn = 'collorg.planning.task_schedule' ),
   task C_OID,
   FOREIGN KEY(task) REFERENCES "collorg.planning".task(cog_oid),
   schedule_oid C_OID NOT NULL,
   schedule_fqtn STRING NOT NULL
       CHECK(schedule_fqtn like 'collorg.planning.scheduler'),
   FOREIGN KEY(schedule_oid, schedule_fqtn)
       REFERENCES "collorg.core".oid_table(cog_oid, cog_fqtn),
   editable STRING,
   original BOOL DEFAULT 'f',
   PRIMARY KEY(task, schedule_oid)
) INHERITS( "collorg.core".base_table );
