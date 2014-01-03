#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Lost_found(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.core.view'
    _cog_tablename = 'lost_found'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * cog_oid_ : c_oid
        * cog_fqtn_ : c_fqtn
        * bt_cog_oid_ : c_oid
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Lost_found, self).__init__(db, **kwargs)

    def check(self):
        self.bt_cog_oid_.set_null()
        for elt in self:
            print "missing: {} {}".format(self.cog_oid_, self.cog_fqtn_)

    def clean(self, interactive=True):
        total = self.count()
        self.bt_cog_oid_.set_null()
        to_remove = self.count()
        print("About to remove {} elements from {}.".format(
            to_remove, total))
        ok = raw_input("Proceed [Y/n] ? ")
        if ok == '' or ok.upper() == 'Y':
            oid_table = self.db.table('collorg.core.oid_table')
            oid_table.cog_oid_.set_intention(self.cog_oid_)
            oid_table.delete()
