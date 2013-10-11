CREATE TABLE "collorg.auth".d_ldap (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.auth.d_ldap' CHECK( cog_fqtn = 'collorg.auth.d_ldap' ),
   domain STRING NOT NULL,
   host STRING NOT NULL,
   port SMALLINT,
   account STRING,
   password PASSWORD,
   connectivity_security C_OID,
   FOREIGN KEY(connectivity_security) REFERENCES "collorg.core".checked_val(cog_oid),
   -- CHECK(connectivity_security = 'LDAPS' or connectivity_security = 'START_TLS'),
   certificate_checks C_OID,
   FOREIGN KEY(certificate_checks) REFERENCES "collorg.core".checked_val(cog_oid),
   -- CHECK(certificate_checks = 'NEVER' or
   --  certificate_checks = 'ALLOW' or
   --  certificate_checks = 'TRY' or
   --  certificate_checks = 'DEMAND' or
   --  certificate_checks = 'HARD') DEFAULT 'NEVER',
   base_dn STRING NOT NULL,
   organizational_unit STRING NOT NULL,
   filter STRING,
   scope C_OID,
   -- CHECK(scope = 'BASE' or scope = 'ONELEVEL' or scope = 'SUBTREE'),
   FOREIGN KEY(scope) REFERENCES "collorg.core".checked_val(cog_oid),
   login_attr STRING NOT NULL DEFAULT 'uid',
   first_name_attr STRING,
   last_name_attr STRING,
   e_mail_attr STRING DEFAULT 'mail',
   "default" BOOL DEFAULT 't',
   UNIQUE("host", "base_dn", "filter"),
   PRIMARY KEY(domain)
) INHERITS( "collorg.core".base_table ) ;

