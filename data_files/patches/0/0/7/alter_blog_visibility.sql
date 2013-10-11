ALTER TABLE "collorg.communication".blog ADD column visibility string NOT NULL default 'private';
ALTER TABLE "collorg.communication".blog ADD constraint visibility_visibility_check CHECK ( visibility in ( 'private', 'protected', 'public'));
ALTER TABLE "collorg.communication".blog INHERIT "collorg.access".visibility;
