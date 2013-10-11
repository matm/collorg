#-*- coding: UTF-8 -*-

from collorg.db.communication.blog.post import Post

class Event(Post):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.event'
    _cog_tablename = 'event'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _location_ = cog_r._location_
    #<<< AUTO_COG REL_PART. Your code goes after
    __is_cog_event = True
    __event_types = None
    __cog_type_name = 'Event'
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
        * introductory_paragraph_ : string
        * text_ : wiki, inherited, not null
        * author_ : c_oid, inherited, not null
        * public_ : bool, inherited
        * comment_ : bool, inherited
        * expiry_date_ : timestamp, inherited
        * important_ : bool, inherited
        * broadcast_ : bool, inherited
        * visibility_ : string, not null
        * begin_date_ : timestamp, not null
        * end_date_ : timestamp, not null
        * location_ : c_oid, FK
        * other_location_ : wiki
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Event, self).__init__(db, **kwargs)

    @property
    def _cog_label(self):
        return ['<img src="/collorg/images/alarm.svg" '
                'class="medicon" alt="event" /> {} {}',
                self.title_, self.begin_date_.value.strftime('%Y-%m-%d')]

    def get_event_types(self):
        if self._Event__event_types is not None:
            return self._Event__event_types
        self._Event__event_types = []
        for fqtn in self.db.fqtns:
            obj = self.db.table(fqtn)
            if hasattr(obj, '_Event__is_cog_event'):
                self._Event__event_types.append(obj)
        return self._Event__event_types

    def winsert(self, user, **kwargs):
        self.begin_date_.set_intention(kwargs['begin_date_'])
        self.end_date_.set_intention(kwargs['end_date_'])
        self = super(Event, self).winsert(user, **kwargs)
        return self

    def wupdate(self, **kwargs):
        n_event = self()
        n_event.begin_date_.set_intention(kwargs['begin_date_'])
        n_event.end_date_.set_intention(kwargs['end_date_'])
        self = super(Event, self).wupdate(n_event, **kwargs)
        return self

    def add_see_also(self, **kwargs):
        return super(self.__class__, self).add_see_also(**kwargs)
