CREATE TABLE "collorg.communication.blog".post (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.communication.blog.post'
      CHECK( cog_fqtn = 'collorg.communication.blog.post' ) NO INHERIT,
   title STRING NOT NULL,
   introductory_paragraph STRING default '',
   text WIKI NOT NULL,
   author C_OID NOT NULL,
   constraint "author"
   FOREIGN KEY (author) REFERENCES "collorg.actor"."user"(cog_oid),
   public BOOLEAN DEFAULT 'f',
   comment BOOLEAN DEFAULT 'f',
   expiry_date timestamp(0),
   important boolean default 'f',
   broadcast boolean default 'f',
   visibility STRING NOT NULL
     CHECK (visibility IN ('private', 'protected', 'public')) default 'private',
   PRIMARY KEY(cog_oid)
)INHERITS("collorg.core".base_table);
