CREATE TABLE "collorg.communication.blog".a_post_data (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.communication.blog.a_post_data'
      CHECK( cog_fqtn = 'collorg.communication.blog.a_post_data' ),
   post c_oid,
   FOREIGN KEY(post) REFERENCES "collorg.core".oid_table(cog_oid),
--   FOREIGN KEY(post) REFERENCES "collorg.communication.blog".oid_post(cog_oid),
   data c_oid,
   FOREIGN KEY(data) REFERENCES "collorg.core".oid_table(cog_oid),
   who c_oid,
   FOREIGN KEY(who) REFERENCES "collorg.actor"."user"(cog_oid),
   "when" timestamp(0) default ('now'::text)::timestamp(0) with time zone,
   private_reference boolean default 'f',
   "order" int,
   see_also boolean default 'f',
   PRIMARY KEY(post, data)
) INHERITS( "collorg.core".base_table );

-- mettre du code trigger pour vérifier que le parent est de type evenement
-- on fait confiance au programmeur pour l'instant
