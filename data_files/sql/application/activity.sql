-- abstract

CREATE TABLE "collorg.application".activity (
   cog_oid C_OID UNIQUE NOT NULL,
   cog_fqtn C_FQTN NOT NULL DEFAULT 'collorg.application.activity'
   CHECK( cog_fqtn != 'collorg.application.activity' )
) INHERITS( "collorg.core".base_table ) ;

