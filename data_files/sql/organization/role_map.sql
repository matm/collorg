CREATE TABLE "collorg.organization".role_map (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.organization.role_map'
      CHECK( cog_fqtn = 'collorg.organization.role_map' ),
   appointer C_OID NOT NULL,
   FOREIGN KEY( appointer ) REFERENCES "collorg.actor".role( cog_oid ),
   appointee C_OID NOT NULL,
   FOREIGN KEY( appointee ) REFERENCES "collorg.actor".role( cog_oid ),
   PRIMARY KEY( appointer, appointee )
) INHERITS( "collorg.core".base_table ) ;

