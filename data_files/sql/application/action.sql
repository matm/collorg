CREATE TABLE "collorg.application".action (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.application.action' CHECK( cog_fqtn = 'collorg.application.action' ),
   "data_type" C_FQTN NOT NULL,
      FOREIGN KEY( "data_type" ) REFERENCES "collorg.core"."data_type"( fqtn ) ON UPDATE CASCADE,
   name STRING NOT NULL,
   label STRING,
   description WIKI,
   format STRING DEFAULT 'html',
   source TEXT,
   "raw" boolean default 'f',
   protected BOOLEAN DEFAULT 't',
   in_menu BOOLEAN DEFAULT 'f',
   in_header BOOLEAN DEFAULT 'f',
   in_nav boolean default 'f',
   write boolean default 'f',
   moderate boolean default 'f',
   admin boolean default 'f',
   icon STRING,
   this_application boolean default 't',
   PRIMARY KEY( name, "data_type" )
) INHERITS( "collorg.core".base_table ) ;

