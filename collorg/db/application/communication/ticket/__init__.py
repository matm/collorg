#-*- coding: UTF-8 -*-

from collorg.db.communication.blog.post import Post

class Ticket(Post):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application.communication'
    _cog_tablename = 'ticket'
    _cog_templates_loaded = False

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
        * title_ : string, inherited, not null
        * introductory_paragraph_ : string, inherited
        * text_ : wiki, inherited, not null
        * author_ : c_oid, inherited, not null
        * public_ : bool, inherited
        * comment_ : bool, inherited
        * expiry_date_ : timestamp, inherited
        * important_ : bool, inherited
        * broadcast_ : bool, inherited
        * visibility_ : string, inherited, not null
        * kind_ : ticket_kind
        * priority_ : ticket_priority
        * status_ : ticket_status
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Ticket, self).__init__(db, **kwargs)

