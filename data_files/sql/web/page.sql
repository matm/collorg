CREATE TABLE "collorg.web".page (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN
      DEFAULT 'collorg.web.page' CHECK( cog_fqtn = 'collorg.web.page' ),
   site C_OID,
   FOREIGN KEY(site) REFERENCES "collorg.web".site(cog_oid),
   path_info STRING NOT NULL,
   title STRING,
   label TEXT NOT NULL,
   content WIKI,
   environment c_oid,
   CONSTRAINT "environment"
     FOREIGN KEY(environment) REFERENCES "collorg.core".oid_table(cog_oid),
   data_type c_fqtn,
   CONSTRAINT "data_type"
     FOREIGN KEY(data_type) REFERENCES "collorg.core".data_type(fqtn),
   PRIMARY KEY(site, path_info)
) INHERITS( "collorg.core".base_table ) ;

-- une page est définie par son chemin dans le site (path_info).
-- le source de la page est stocké sous la forme d'une méthode w3display
-- dans l'arbo .../web/cog_templates/page/__src/un/chemin/etc
-- http://site/un fera référence à la page définie par :
--  .../web/cog_templates/__src/page/un/w3display ->
--  .../web/cog_templates/page/un/w3display.py
-- contrainte :
-- le path_info devra pouvoir être traduit en un chemin python : /page/un ->
-- from page.un import w3display
