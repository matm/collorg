CREATE TABLE "collorg.actor"."user" (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.actor.user' CHECK( cog_fqtn LIKE 'collorg.actor.user%' ),
   first_name STRING NOT NULL,
   last_name STRING NOT NULL,
   gender CHARACTER CHECK( gender = 'F' or gender = 'M' or gender = ''),
   birthday DATE,
   email EMAIL UNIQUE NOT NULL,
   pseudo TEXT UNIQUE,
   password PASSWORD NOT NULL,
   validation_key C_OID NOT NULL,--UNIQUE NOT NULL,
   valid_account BOOLEAN DEFAULT 'f',
   system_account BOOLEAN DEFAULT 'f',
   ldap C_OID,
   FOREIGN KEY(ldap) REFERENCES "collorg.auth".d_ldap(cog_oid),
   photo C_OID,
   -- FOREIGN KEY(photo) REFERENCES "collorg.communication".file(cog_oid),
   -- after see user_s_photo.sql for the FK definition
   -- biography WIKI,
   "url" url,
   alien boolean default 'f',
   PRIMARY KEY( email )
) INHERITS( "collorg.actor"."actor" ) ;
