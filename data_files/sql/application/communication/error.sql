CREATE TABLE "collorg.application.communication".error (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.application.communication.error'
      CHECK( cog_fqtn = 'collorg.application.communication.error' ),
   hit INT DEFAULT 1,
   PRIMARY KEY(title)
) INHERITS( "collorg.application.communication".ticket );
