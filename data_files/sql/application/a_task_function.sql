CREATE TABLE "collorg.application".a_task_function (
   function C_OID NOT NULL,
   FOREIGN KEY( function ) REFERENCES "collorg.actor".function( cog_oid ),
   task C_OID NOT NULL,
   FOREIGN KEY( task ) REFERENCES "collorg.application".task( cog_oid ),
   description WIKI,
   PRIMARY KEY( function, task )
);
