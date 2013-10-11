CREATE TABLE "collorg.communication".file (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.communication.file'
      CHECK( cog_fqtn = 'collorg.communication.file' ),
   uploader C_OID NOT NULL,
   FOREIGN KEY (uploader) REFERENCES "collorg.actor"."user"( cog_oid ),
   name STRING NOT NULL,
   signature STRING UNIQUE NOT NULL,
   size STRING,
   visibility string default 'protected'
     check (visibility in ('private', 'protected', 'public')),
   PRIMARY KEY(signature)
)INHERITS("collorg.core".base_table);
