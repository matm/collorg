CREATE TABLE "collorg.communication.blog".see_also (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.communication.blog.see_also'
      CHECK( cog_fqtn = 'collorg.communication.blog.see_also' ),
   post c_oid,
   FOREIGN KEY(post) REFERENCES "collorg.core".oid_table(cog_oid),
--   FOREIGN KEY(post) REFERENCES "collorg.communication.blog".oid_post(cog_oid),
   data c_oid,
   FOREIGN KEY(data) REFERENCES "collorg.core".oid_table(cog_oid),
   PRIMARY KEY(post, data)
) INHERITS( "collorg.core".base_table );

-- mettre du code trigger pour vérifier que le parent est de type evenement
-- on fait confiance au programmeur pour l'instant
