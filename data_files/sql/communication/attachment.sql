CREATE TABLE "collorg.communication".attachment (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.communication.attachment'
      CHECK( cog_fqtn = 'collorg.communication.attachment' ),
   author C_OID NOT NULL,
   FOREIGN KEY (author) REFERENCES "collorg.actor"."user"( cog_oid ),
   ref C_OID NOT NULL,
   FOREIGN KEY (ref) REFERENCES "collorg.communication".file( cog_oid ),
   description WIKI,
   data C_OID NOT NULL,
   FOREIGN KEY (data) REFERENCES "collorg.core".oid_table(cog_oid),
   PRIMARY KEY(ref, data) -- only one attachment with ref for a given data
)INHERITS("collorg.core".base_table);
