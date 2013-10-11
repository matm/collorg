update "collorg.application".action set write = 't' where cog_oid in (select cog_oid from "collorg.access.view".access_ca where task_name = 'Blog edition');
