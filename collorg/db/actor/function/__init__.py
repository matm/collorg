#-*- coding: utf-8 -*-

from collorg.db.actor.actor import Actor

class Function( Actor ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.actor'
    _cog_tablename = 'function'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _data_type_ = cog_r._data_type_
    # REVERSE
    _rev_a_function_category_ = cog_r._rev_a_function_category_
    _rev_a_function_inst_group_ = cog_r._rev_a_function_inst_group_
    _rev_role_ = cog_r._rev_role_
    _rev_a_task_function_ = cog_r._rev_a_task_function_
    _rev_definition_ = cog_r._rev_definition_
    _rev_a_topic_function_ = cog_r._rev_a_topic_function_
    #<<< AUTO_COG REL_PART. Your code goes after
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
        * name_ : string, uniq, not null
        * fname_ : string, not null
        * long_name_ : string, PK, not null
        * advertise_ : bool
        * data_type_ : c_fqtn, uniq, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Function, self ).__init__( db, **kwargs )

    @property
    def _cog_label(self):
        return ['{}', self.long_name_]

    def users(self, data = None):
        """returns the users having the function on data. None if no one"""
        access = self._rev_role_._access_
        access._data_ = data
        access.granted()
        if not access.is_empty():
            return access._user_
