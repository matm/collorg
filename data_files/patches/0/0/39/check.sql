CREATE TABLE "collorg.application".check (
   description WIKI,
   requires C_OID NOT NULL,
   FOREIGN KEY( requires ) REFERENCES "collorg.application".action( cog_oid ),
   required C_OID NOT NULL,
   FOREIGN KEY( required ) REFERENCES "collorg.application".action( cog_oid ),
   PRIMARY KEY( requires, required )
);
