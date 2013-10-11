CREATE TABLE "collorg.group"."a_wg_template_role" (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.group.a_wg_template_role' 
      CHECK( cog_fqtn = 'collorg.group.a_wg_template_role' ),
   template C_OID NOT NULL,
   FOREIGN KEY(template) REFERENCES "collorg.group"."wg_template"(cog_oid),
   role C_OID NOT NULL,
   FOREIGN KEY(role) REFERENCES "collorg.actor"."role"(cog_oid),
   PRIMARY KEY(template, role)
) INHERITS( "collorg.core".base_table ) ;

