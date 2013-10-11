DROP VIEW "collorg.communication.view".inst_tag;
set search_path = "collorg.communication", "collorg.core";
CREATE VIEW "collorg.communication.view".inst_tag AS
SELECT DISTINCT
count(atp),
atp.tag,
atp.inst_tag,
atp.data_type,
atp.status,
data_type.description AS dt_description
FROM
a_tag_post atp
JOIN
data_type ON
atp.data_type = data_type.fqtn
GROUP BY
atp.tag, atp.inst_tag, atp.data_type, atp.status, data_type.description
ORDER BY
atp.data_type, atp.tag;
