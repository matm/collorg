create table "collorg.application.communication".error_traceback (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.application.communication.error_traceback'
      CHECK( cog_fqtn = 'collorg.application.communication.error_traceback' ),
   error C_OID NOT NULL,
   FOREIGN KEY(error)
   REFERENCES "collorg.application.communication".error(cog_oid),
   trace text,
   trace_md5 string,
   hit int DEFAULT 1,
   primary key(error, trace_md5)
) INHERITS( "collorg.core".base_table );
