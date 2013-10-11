CREATE TABLE "collorg.actor".a_function_category (
   function C_OID NOT NULL,
   FOREIGN KEY( function ) REFERENCES "collorg.actor".function( cog_oid ),
   category C_OID NOT NULL,
   FOREIGN KEY( category ) REFERENCES "collorg.actor".category( cog_oid ),
   description WIKI,
   PRIMARY KEY( function, category )
);
