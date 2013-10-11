#-*- coding: UTF-8 -*-

from collorg.db.core.base_table import Base_table

class A_tag_post(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication'
    _cog_tablename = 'a_tag_post'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _data_type_ = cog_r._data_type_
    _post_ = cog_r._post_
    _tag_ = cog_r._tag_
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
        * tag_ : string, PK, not null, FK
        * post_ : c_oid, PK, not null, FK
        * order_ : int4
        * data_type_ : c_fqtn, FK
        * status_ : string
        * inst_tag_ : bool
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(A_tag_post, self).__init__(db, **kwargs)

