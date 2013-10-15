#-*- coding: UTF-8 -*-

import time
from collorg.db.core.base_table import Base_table

class Attachment(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication'
    _cog_tablename = 'attachment'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _data_ = cog_r._data_
    _ref_ = cog_r._ref_
    _author_ = cog_r._author_
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
        * author_ : c_oid, not null, FK
        * ref_ : c_oid, PK, not null, FK
        * description_ : wiki
        * data_ : c_oid, PK, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Attachment, self).__init__(db, **kwargs)

    def attach(self, elt, data, author, description):
        self.ref_.set_intention(elt.cog_oid_.value)
        self._data_ = data
        if self.exists():
            time.sleep(1)
            return "document alread attached"
        self._author_ = author
        self.description_.set_intention(description)
        self.insert()
        time.sleep(1)
        return "document attached"

