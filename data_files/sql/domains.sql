CREATE DOMAIN C_OID AS CHARACTER(36);
CREATE DOMAIN C_FQTN AS TEXT;
CREATE DOMAIN EMAIL AS TEXT;
CREATE DOMAIN PASSWORD AS TEXT;
CREATE DOMAIN WIKI AS TEXT;
CREATE DOMAIN HTML AS TEXT;
CREATE DOMAIN STRING AS TEXT;
CREATE DOMAIN LATEX AS TEXT;
CREATE DOMAIN URL AS TEXT;

CREATE TYPE MONTH AS ENUM('1','2','3','4','5','6','7','8','9','10','11','12');
CREATE TYPE DAY AS ENUM(
'1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16',
'17','18','19','20','21','22','23','24','25','26','27','28','29','30','31');
CREATE TYPE HOUR AS ENUM(
'0','1','2','3','4','5','6',
'7','8','9','10','11','12',
'13','14','15','16','17','18',
'19','20','21','22','23');

CREATE TYPE MINUTE AS ENUM(
'0','1','2','3','4','5','6','7','8','9',
'10','11','12','13','14','15','16','17','18','19',
'20','21','22','23','24','25','26','27','28','29',
'30','31','32','33','34','35','36','37','38','39',
'40','41','42','43','44','45','46','47','48','49',
'50','51','52','53','54','55','56','57','58','59');

create domain percentage int check(value >= 0 and value <= 100);