#-*- coding: UTF-8 -*-

from collorg.db.core.base_table import Base_table

class A_post_data(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication.blog'
    _cog_tablename = 'a_post_data'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _post_ = cog_r._post_
    _data_ = cog_r._data_
    _who_ = cog_r._who_
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
        * post_ : c_oid, PK, not null, FK
        * data_ : c_oid, PK, not null, FK
        * who_ : c_oid, FK
        * when_ : timestamp
        * private_reference_ : bool
        * order_ : int4
        * see_also_ : bool
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(A_post_data, self).__init__(db, **kwargs)

    def insert(self, **kwargs):
        data = self.db.get_elt_by_oid(self.data_.value)
        inc_apd = data._rev_a_post_data_data_
        inc_apd.increment(inc_apd.order_)
        try:
            self.order_.set_intention(0)
            super(self.__class__, self).insert(**kwargs)
            self._data_.get()._wipe_cache()
            self._post_.get()._wipe_cache()
        except Exception as e:
            raise RuntimeError(e)

    def delete(self, **kwargs):
        try:
            if self._data_.cog_oid_.value:
                self._data_.get()._wipe_cache()
            if self._post_.cog_oid_.value:
                self._post_.get()._wipe_cache()
            super(self.__class__, self).delete(**kwargs)
        except Exception as e:
            raise RuntimeError(e)
