CREATE TABLE "collorg.application".a_task_goal (
   task C_OID NOT NULL,
   FOREIGN KEY( task ) REFERENCES "collorg.application".task( cog_oid ),
   goal C_OID NOT NULL,
   FOREIGN KEY( goal ) REFERENCES "collorg.application".goal( cog_oid ),
   PRIMARY KEY( task, goal )
);
