CREATE TABLE "collorg.actor"."actor" (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.actor.actor' CHECK(
          cog_fqtn like 'collorg.actor.%' and cog_fqtn != 'collorg.actor.actor' )
) INHERITS( "collorg.core".base_table ) ;
