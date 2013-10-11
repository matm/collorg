CREATE TABLE "collorg.communication".blog (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.communication.blog'
      CHECK( cog_fqtn = 'collorg.communication.blog' ),
   author C_OID NOT NULL,
   FOREIGN KEY (author) REFERENCES "collorg.actor"."user"( cog_oid ),
   title STRING NOT NULL,
   text WIKI NOT NULL,
   data C_OID NOT NULL,
   FOREIGN KEY (data) REFERENCES "collorg.core".oid_table(cog_oid),
   PRIMARY KEY(cog_oid)
)INHERITS("collorg.core".base_table);
