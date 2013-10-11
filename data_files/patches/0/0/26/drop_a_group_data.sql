drop table "collorg.access".a_group_data;
delete from "collorg.core".data_type where fqtn = 'collorg.access.a_group_data';
delete from "collorg.core".field where fqfn like 'collorg.access.a_group_data.%';
