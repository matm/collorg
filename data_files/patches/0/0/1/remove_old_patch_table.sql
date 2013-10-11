DROP TABLE "collorg.core.patch".log;
DELETE FROM "collorg.core".field WHERE fqfn like 'collorg.core.patch.log%' ;
DELETE FROM "collorg.core".data_type WHERE fqtn = 'collorg.core.patch.log' ;
