CREATE TABLE "collorg.location".address (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.location.address'
      CHECK( cog_fqtn = 'collorg.location.address' ),
   address_id C_OID,
   line_1 STRING NOT NULL,
   line_2 STRING,
   line_3 STRING,
   city STRING NOT NULL,
   county_province STRING,
   zip_or_postcode STRING,
   country STRING NOT NULL,
   other_address_details STRING
) INHERITS( "collorg.core".base_table );
