ALTER TABLE "collorg.communication.blog".post DROP CONSTRAINT "post_cog_fqtn_check" ;
ALTER TABLE "collorg.communication.blog".post ADD constraint post_cog_fqtn_check CHECK(cog_fqtn = 'collorg.communication.blog.post') NO INHERIT;
