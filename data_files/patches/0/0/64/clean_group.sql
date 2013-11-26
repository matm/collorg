delete from "collorg.planning".calendar;

delete from "collorg.group"."group" where name like 'Directeur de thèse';
delete from "collorg.group"."group" where name like 'Encadrant de thèse';
delete from "collorg.group"."group" where name like 'Responsable%';
delete from "collorg.group"."group" where name like 'Permanent%';
delete from "collorg.group"."group" where name like 'Doctorant%';
delete from "collorg.group"."group" where name like 'tmp%';

delete from "collorg.core".oid_table where cog_oid not in (select cog_oid from "collorg.core".base_table );
