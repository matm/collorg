#-*- coding: UTF-8 -*-

import hashlib

from collorg.db.core.base_table import Base_table

class Error_traceback(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application.communication'
    _cog_tablename = 'error_traceback'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _error_ = cog_r._error_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : c_oid, uniq, not null
        * cog_fqtn_ : c_fqtn, not null
        * cog_signature_ : text, inherited
        * cog_test_ : bool, inherited
        * cog_creat_date_ : timestamp, inherited
        * cog_modif_date_ : timestamp, inherited
        * cog_environment_ : c_oid, inherited
        * cog_state_ : text, inherited
        * error_ : c_oid, PK, not null, FK
        * trace_ : text
        * trace_md5_ : string, PK, not null
        * hit_ : int4
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Error_traceback, self).__init__(db, **kwargs)

    def hit(self, traceback):
        self.trace_.value = traceback
        self.trace_md5_.value = hashlib.md5(traceback).hexdigest()
        if self.is_empty():
            self.insert()
        else:
            nself = self()
            nself.hit_.value = self.get().hit_.value + 1
            self.update(nself)
