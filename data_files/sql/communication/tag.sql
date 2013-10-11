CREATE TABLE "collorg.communication".tag (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.communication.tag'
      CHECK( cog_fqtn = 'collorg.communication.tag' ),
   tag STRING NOT NULL,
   PRIMARY KEY(tag)
)INHERITS("collorg.core".base_table);
