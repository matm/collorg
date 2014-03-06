#-*- coding: utf-8 -*-

from collections import OrderedDict
from collorg.db.core.base_table import Base_table

class Site( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.web'
    _cog_tablename = 'site'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # REVERSE
    _rev_topic_ = cog_r._rev_topic_
    #<<< AUTO_COG REL_PART. Your code goes after
    d_topics = None
    def __init__( self, db, **kwargs ):
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
        * url_ : url, PK, not null
        * title_ : string
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Site, self ).__init__( db, **kwargs )

    @property
    def _cog_label(self):
        return ["{}", self.url_]

    def load_topic(self, url = None, path_info = None):
        if not path_info:
            path_info = '/'
        if url:
            self.url_.value = url
        if self.is_empty():
            url = self.db._cog_params['url']
            self.url_.value = url
        self = self.get() # 1 site !!!!
        topic = self.db.table('collorg.web.topic')
        topic.site_.value = self.cog_oid_.value
        topic.path_info_.value = path_info
        if topic.count() == 1:
            topic = topic.get()
        else:
            topic.path_info_.value = '/'
            topic = topic.get()
        return topic, topic.w3display

    def load_topics(self):
        #XXX TO update if modification on topics
        #XXX must tag the site to be reloaded to trigger reload of
        #XXX topics on each process running.
        if Site.d_topics is None:
            Site.d_topics = OrderedDict()
            self = self.get()
            topics = self._rev_topic_
            topics.order_by(topics.path_info_)
            for topic in topics:
                Site.d_topics[topic.path_info_.value] = (topic, topic.w3display)
        return Site.d_topics
