#-*- coding: UTF-8 -*-

from collorg.orm.table import Table
from datetime import datetime

class By_post(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication.blog.view'
    _cog_tablename = 'by_post'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : c_oid
        * cog_fqtn_ : c_fqtn
        * post_order_ : int4
        * post_creat_date_ : timestamp
        * event_begin_date_ : timestamp
        * post_modif_date_ : timestamp
        * post_title_ : string
        * introductory_paragraph_ : string
        * public_post_ : bool
        * post_visibility_ : string
        * important_post_ : bool
        * broadcast_post_ : bool
        * expiry_date_ : timestamp
        * author_topic_oid_ : c_oid
        * author_oid_ : c_oid
        * author_first_name_ : string
        * author_last_name_ : string
        * data_oid_ : c_oid
        * attachment_ : int8
        * comment_ : int8
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(By_post, self).__init__(db, **kwargs)

    def get_link_label(self, list_elt):
        """
        list_elt is a cog_light elt...
        """
        begin_date = list_elt.event_begin_date_ or ""
        create_date = list_elt.post_creat_date_
        link = list_elt.post_title_
        if begin_date and begin_date != create_date:
            link = ('<img src="/collorg/images/alarm.svg" '
                'class="medicon" alt="event" /> {}<br>{}'.format(
                    list_elt.post_title_,
                    begin_date.strftime("%Y-%m-%d @ %H:%M")))
        elif list_elt.cog_fqtn_ == 'collorg.web.topic':
            link = ('<img src="/collorg/images/folder.png" /> {}'.format(
                list_elt.post_title_))
        return link
