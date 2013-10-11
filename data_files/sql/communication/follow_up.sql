CREATE TABLE "collorg.communication".follow_up (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.communication.follow_up'
      CHECK( cog_fqtn = 'collorg.communication.follow_up' ),
   author C_OID NOT NULL,
   FOREIGN KEY (author) REFERENCES "collorg.actor"."user"( cog_oid ),
   text WIKI NOT NULL,
   comment C_OID NOT NULL,
   FOREIGN KEY (comment) REFERENCES "collorg.communication".comment(cog_oid),
   PRIMARY KEY(cog_oid)
)INHERITS("collorg.core".base_table);
