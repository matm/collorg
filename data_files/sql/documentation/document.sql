CREATE TABLE "collorg.documentation".document (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.documentation.document'
      CHECK( cog_fqtn = 'collorg.documentation.document' ),
   author C_OID,
   FOREIGN KEY ( author ) REFERENCES "collorg.actor"."user"( cog_oid ),
   language C_OID,
   FOREIGN KEY ( language ) REFERENCES "collorg.i18n".language( cog_oid ),
   title STRING NOT NULL,
   data_oid C_OID NOT NULL,
   data_fqtn TEXT NOT NULL,
   summary STRING
   -- date de création, versioning, ...
   -- #!! pas complet
)INHERITS("collorg.core".base_table);
