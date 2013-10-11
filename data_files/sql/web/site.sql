CREATE TABLE "collorg.web".site (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.web.site' CHECK( cog_fqtn = 'collorg.web.site' ),
   url URL NOT NULL,
   title STRING,
   PRIMARY KEY(url)
) INHERITS( "collorg.core".base_table ) ;
