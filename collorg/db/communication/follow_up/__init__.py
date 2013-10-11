#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table

class Follow_up(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication'
    _cog_tablename = 'follow_up'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _comment_ = cog_r._comment_
    _author_ = cog_r._author_
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
        * comment_ : c_oid, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Follow_up, self).__init__(db, **kwargs)

    @property
    def view_list(self):
        raise NotImplementedError
        user = self._author_
        view = self.db.pview(
            self.cog_oid_,
            self.cog_creat_date_.name_as('creat_date'),
            self.cog_modif_date_.name_as('modif_date'),
            self.text_,
            user.cog_oid_.name_as('user_oid'),
            user.first_name_,
            user.last_name_)
        view.creat_date_.set_descending_order()
        view.order_by(view.creat_date_)
        return view
