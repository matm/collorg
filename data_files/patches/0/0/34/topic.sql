CREATE TABLE "collorg.web".topic (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.web.topic'
      CHECK( cog_fqtn = 'collorg.web.topic' ),
   path_info STRING NOT NULL,
   environment c_oid,
   CONSTRAINT "environment"
     FOREIGN KEY(environment) REFERENCES "collorg.core".oid_table(cog_oid),
   data_type c_fqtn,
   CONSTRAINT "data_type"
     FOREIGN KEY(data_type) REFERENCES "collorg.core".data_type(fqtn),
   constraint "author"
   FOREIGN KEY (author) REFERENCES "collorg.actor"."user"(cog_oid),
   PRIMARY KEY(environment, path_info)
) INHERITS( "collorg.communication.blog".post );

alter table "collorg.web".topic alter column text set default '';

