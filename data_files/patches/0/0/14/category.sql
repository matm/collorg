CREATE TABLE "collorg.actor".category (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.actor.category'
      CHECK(cog_fqtn = 'collorg.actor.category'),
   label STRING NOT NULL,
   parent_oid C_OID,
   expiration_date DATE,
   FOREIGN KEY(parent_oid)
     REFERENCES "collorg.actor".category(cog_oid),
   UNIQUE(label, parent_oid),
   PRIMARY KEY (cog_oid)
) INHERITS("collorg.core".base_table) ;
