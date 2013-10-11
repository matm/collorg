CREATE TABLE "collorg.activity".a_task_goal (
   task C_OID NOT NULL,
   FOREIGN KEY( task ) REFERENCES "collorg.activity".task( cog_oid ),
   goal C_OID NOT NULL,
   FOREIGN KEY( goal ) REFERENCES "collorg.activity".goal( cog_oid ),
   PRIMARY KEY( task, goal )
);
