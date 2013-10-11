CREATE TABLE "collorg.documentation".comment (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.documentation.comment'
      CHECK( cog_fqtn = 'collorg.documentation.comment' ),
   author C_OID NOT NULL,
   FOREIGN KEY ( author ) REFERENCES "collorg.actor"."user"( cog_oid ),
   text WIKI NOT NULL,
   part C_OID NOT NULL,
   FOREIGN KEY ( part ) REFERENCES "collorg.documentation".part( cog_oid )
)INHERITS("collorg.core".base_table);
