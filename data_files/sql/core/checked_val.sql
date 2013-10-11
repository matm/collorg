CREATE TABLE "collorg.core".checked_val (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.core.checked_val' CHECK( cog_fqtn = 'collorg.core.checked_val' ),
   field STRING NOT NULL,
   FOREIGN KEY(field) REFERENCES "collorg.core".field(fqfn),
   val STRING NOT NULL,
   "default" BOOL DEFAULT 'f', 
   PRIMARY KEY(field, val)
) INHERITS( "collorg.core".base_table ) ;
