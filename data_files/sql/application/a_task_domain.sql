CREATE TABLE "collorg.application".a_task_domain (
   task C_OID NOT NULL,
   FOREIGN KEY( task ) REFERENCES "collorg.application".task( cog_oid ),
   domain C_OID NOT NULL,
   FOREIGN KEY( domain ) REFERENCES "collorg.application".domain( cog_oid ),
   PRIMARY KEY( task, domain )
);
