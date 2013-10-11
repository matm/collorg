CREATE TABLE "collorg.communication".comment (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.communication.comment'
      CHECK( cog_fqtn = 'collorg.communication.comment' ),
   author C_OID NOT NULL,
   FOREIGN KEY (author) REFERENCES "collorg.actor"."user"( cog_oid ),
   text WIKI NOT NULL,
   data C_OID NOT NULL,
   FOREIGN KEY (data) REFERENCES "collorg.core".oid_table(cog_oid),
   field STRING,
   FOREIGN KEY (field) REFERENCES "collorg.core".field(fqfn),
   PRIMARY KEY(cog_oid)
)INHERITS("collorg.core".base_table);
