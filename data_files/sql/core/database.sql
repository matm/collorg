CREATE TABLE "collorg.core".database(
    cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
    cog_fqtn C_FQTN
       DEFAULT 'collorg.core.database' CHECK( cog_fqtn = 'collorg.core.database' ),
    name STRING PRIMARY KEY,
    long_name TEXT UNIQUE,
    release INT,
    sub_release INT,
    description WIKI
) INHERITS( "collorg.core".base_table ) ;
