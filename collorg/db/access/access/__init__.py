#-*- coding: utf-8 -*-
### Copyright © 2011 Joël Maïzi <joel.maizi@lirmm.fr>
### This file is part of collorg

### collorg is free software: you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation, either version 3 of the License, or
### (at your option) any later version.

### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.

### You should have received a copy of the GNU General Public License
### along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collorg.db.core.base_table import Base_table
from datetime import datetime

class Access( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.access'
    _cog_tablename = 'access'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _data_ = cog_r._data_
    _user_ = cog_r._user_
    # REVERSE
    _rev_role_ = cog_r._rev_role_
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
        * cog_from_ : timestamp, inherited
        * cog_to_ : timestamp, inherited
        * user_ : c_oid, PK, not null, FK
        * data_ : c_oid, PK, not null, FK
        * write_ : bool
        * manage_ : bool
        * begin_date_ : timestamp, PK, not null
        * end_date_ : timestamp
        * description_ : wiki
        * pourcentage_ : int4
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Access, self ).__init__( db, **kwargs )

    def __get_user(self):
        return self._user_
    def __set_user(self, user):
        self._user_ = user
    user = property(__get_user, __set_user)

    def __get_data(self):
        return self._data_
    def __set_data(self, data):
        self = self.granted()
        self._data_ = data
    data = property(__get_data, __set_data)

    def __set_at_date(self, date = None):
        """
        contrains the access. used to check whether an access
        is granted at a certain date
        """
        if not date:
            date = datetime.now()
        self.begin_date_.set_null()
        self.begin_date_ += (date, '<=')
        self.end_date_.set_null()
        self.end_date_ += (date, '>=')
        return self
    at_date = property(fset=__set_at_date)

    def grant(self,
              user = None, data = None, function = None, write = False,
              pourcentage = None, begin_date = None, end_date = None):
        """
        An access can be granted to a user with a role on a data.
        If begin_date and/or end_date are specified, the access will be granted
        on the [begin_date:end_date] interval. Otherwise, the access is granted
        until it's revoked.
        #!! The granter shoud be registered
        """
        #self.db.set_auto_commit(False)
        if data is not None:
            self._data_ = data
        if user is not None:
            self._user_ = user
        self.write_.set_intention(write)
        if not self.is_granted():
            self.begin_date_.set_intention(begin_date)
            self.end_date_.set_intention(end_date)
            self.pourcentage_.set_intention(pourcentage)
            self.insert()
        if function:
            role = self._rev_role_
            role._function_ = function
            if not role.exists():
                role.insert()
        #self.db.commit()

    def revoke(self, end_date = None):
        """
        The access is revoked by setting the end date to datetime.now()
        We should register the user that has revoked the access
        #!! Who is invoking this method ???
        #!! Where do we store the operations
        """
        self.granted()
        self = self.get()
        this = self()
        this.cog_oid_.set_intention(self.cog_oid_.value)
        self.db.set_auto_commit(False)
        for role in self._rev_role_:
            role.revoke()
        n_access = self()
        n_access.end_date_.set_intention(end_date or datetime.now())
        self.update(n_access)
        self.db.commit()
        if this.get().is_granted():
            raise Exception("Access still granted!")

    def granted(self, begin_date = None, end_date = None):
        self.begin_date_.set_intention(begin_date or datetime.now(), '<')
        self.end_date_.set_null()
        self.end_date_ += (end_date or datetime.now(), '>')
        return self

    def set_pourcentage(self, pct):
        ue = self()
        to_update = self.get(fields=(self.cog_oid_,))
        to_update.cog_oid_.set_intention(self.cog_oid_.value)
        ue.pourcentage_.set_intention(pct)
        to_update.update(ue)

    def is_granted(self):
        """
        Internal checker for granted access.
        self.user_ and self.data_ must be constrained.
        """
        assert self.user_.is_constrained
        assert self.data_.is_constrained
        access = self()
        access.cog_oid_.set_intention(self.cog_oid_)
        access.granted()
        return access.exists()

    def revoke_write(self):
        new_acc = self()
        new_acc.write_.set_intention(False)
        self.update(new_acc)

    def grant_write(self):
        new_acc = self()
        new_acc.write_.set_intention(True)
        self.update(new_acc)
