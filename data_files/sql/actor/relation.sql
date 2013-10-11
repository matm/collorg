CREATE TABLE "collorg.actor".relation (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.actor.relation' CHECK( cog_fqtn = 'collorg.actor.relation' ),
   me C_OID,
   FOREIGN KEY(me) REFERENCES "collorg.actor"."user"(cog_oid),
   my_relation C_OID,
   FOREIGN KEY(my_relation) REFERENCES "collorg.actor"."user"(cog_oid),
   PRIMARY KEY( me, my_relation )
) INHERITS( "collorg.core".base_table ) ;

