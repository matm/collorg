CREATE TABLE "collorg.application".state (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.application.state' CHECK( cog_fqtn = 'collorg.application.state' ),
   value STRING NOT NULL,
   description WIKI,
   data_type C_FQTN NOT NULL,
   FOREIGN KEY(data_type) REFERENCES "collorg.core".data_type(fqtn) ON UPDATE CASCADE,
  PRIMARY KEY( value, data_type )
) INHERITS( "collorg.core".base_table ) ;

