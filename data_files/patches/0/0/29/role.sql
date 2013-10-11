CREATE TABLE "collorg.access"."role" (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.access.role'
      CHECK( cog_fqtn = 'collorg.access.role' ),
   access C_OID NOT NULL,
   constraint "access"
   FOREIGN KEY(access) REFERENCES "collorg.access".access(cog_oid),
   function C_OID NOT NULL,
   constraint "function"
   FOREIGN KEY(function) REFERENCES "collorg.core".oid_table(cog_oid),
   PRIMARY KEY(access, function)
) INHERITS("collorg.core".base_table) ;

