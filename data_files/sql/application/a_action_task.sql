CREATE TABLE "collorg.application".a_action_task (
   action C_OID NOT NULL,
   FOREIGN KEY( action ) REFERENCES "collorg.application".action( cog_oid ),
   task C_OID NOT NULL,
   FOREIGN KEY( task ) REFERENCES "collorg.application".task( cog_oid ),
   delegable BOOLEAN DEFAULT 'f',
   description WIKI,
   PRIMARY KEY( action, task )
);
