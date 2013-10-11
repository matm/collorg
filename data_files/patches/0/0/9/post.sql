CREATE TABLE "collorg.communication.blog".post (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.communication.blog.post'
      CHECK( cog_fqtn = 'collorg.communication.blog.post' ) NO INHERIT,
   title STRING NOT NULL,
   text WIKI NOT NULL,
   author_s_group C_OID NOT NULL,
   FOREIGN KEY (author_s_group) REFERENCES "collorg.group"."group"(cog_oid),
   public BOOLEAN DEFAULT 'f',
   expiration_date timestamp(0),
   important boolean default 'f',
   broadcast boolean default 'f',
   PRIMARY KEY(cog_oid)
)INHERITS("collorg.core".base_table);
