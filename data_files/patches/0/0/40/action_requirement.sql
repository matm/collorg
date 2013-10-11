set search_path to "collorg.application";
create view "collorg.application.view".action_requirement AS
SELECT
requires.cog_oid as requires_oid,
requires.name as requires_name,
requires.data_type as requires_data_type,
required.cog_oid as required_oid,
required.name as required_name,
required.data_type as required_data_type
FROM "check"
join action requires on
"check".requires = requires.cog_oid
join action required on
"check".required = required.cog_oid;
