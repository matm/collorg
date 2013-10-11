CREATE TYPE "ticket_kind" AS ENUM (
       'runtime error', 'bug', 'enhancement', 'proposal', 'task');
CREATE TYPE "ticket_priority" AS ENUM (
       'trivial', 'minor', 'major', 'critical', 'blocker');
CREATE TYPE "ticket_status" AS ENUM (
       'open', 'on hold', 'resolved', 'duplicate', 'invalid', 'wontfix');

CREATE TABLE "collorg.application.communication".ticket (
   cog_oid C_OID UNIQUE NOT NULL,
   FOREIGN KEY(cog_oid) REFERENCES "collorg.core".oid_table(cog_oid)
      INITIALLY DEFERRED,
   cog_fqtn C_FQTN NOT NULL
      DEFAULT 'collorg.application.communication.ticket'
      CHECK( cog_fqtn = 'collorg.application.communication.ticket' ) NO INHERIT,
   kind ticket_kind,
   priority ticket_priority,
   status ticket_status,
   PRIMARY KEY(cog_oid)
) INHERITS( "collorg.communication.blog".post );
