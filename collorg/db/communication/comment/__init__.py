#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class Comment(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication'
    _cog_tablename = 'comment'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _data_ = cog_r._data_
    _field_ = cog_r._field_
    _author_ = cog_r._author_
    # REVERSE
    _rev_follow_up_ = cog_r._rev_follow_up_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : c_oid, PK, not null
        * cog_fqtn_ : c_fqtn, not null
        * cog_signature_ : text, inherited
        * cog_test_ : bool, inherited
        * cog_creat_date_ : timestamp, inherited
        * cog_modif_date_ : timestamp, inherited
        * cog_environment_ : c_oid, inherited
        * cog_state_ : text, inherited
        * author_ : c_oid, not null, FK
        * text_ : wiki, not null
        * data_ : c_oid, not null, FK
        * field_ : string, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Comment, self).__init__(db, **kwargs)

    def attach_follow_up(self, follow_up):
        follow_up._comment_ = self
        follow_up._author_ = self._cog_controller.user
        follow_up.insert()
        return follow_up
