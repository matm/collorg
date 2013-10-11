CREATE TABLE "collorg.actor".a_function_inst_group (
   function C_OID NOT NULL,
   FOREIGN KEY( function ) REFERENCES "collorg.actor".function( cog_oid ),
   inst_group C_OID NOT NULL,
   FOREIGN KEY( inst_group ) REFERENCES "collorg.actor".inst_group( cog_oid ),
   description WIKI,
   PRIMARY KEY( function, inst_group )
);
