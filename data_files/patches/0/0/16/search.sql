CREATE TABLE "collorg.web".search (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.web.search' CHECK( cog_fqtn = 'collorg.web.search' ),
   data_type C_OID,
   FOREIGN KEY(data_type) REFERENCES "collorg.core".data_type(cog_oid),
   icon STRING NOT NULL,
   title STRING NOT NULL,
   PRIMARY KEY(data_type)
) INHERITS( "collorg.core".base_table ) ;
