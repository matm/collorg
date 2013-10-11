CREATE TABLE "collorg.communication".a_tag_post (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.communication.a_tag_post'
      CHECK( cog_fqtn = 'collorg.communication.a_tag_post' ),
   tag STRING NOT NULL,
   FOREIGN KEY (tag) REFERENCES "collorg.communication".tag(tag),
   post C_OID NOT NULL,
   FOREIGN KEY (post) REFERENCES "collorg.core".oid_table(cog_oid),
   "order" INT,
   data_type C_FQTN,
   FOREIGN KEY(data_type) REFERENCES "collorg.core".data_type(fqtn),
   status STRING,
   inst_tag boolean default 'f',
   PRIMARY KEY(tag, post)
)INHERITS("collorg.core".base_table);
