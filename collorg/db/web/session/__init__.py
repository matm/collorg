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

from collorg.orm.table import Table as TClass
from datetime import datetime

class Session( TClass ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.web'
    _cog_tablename = 'session'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _user_ = cog_r._user_
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__( self, db, **kwargs ):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * key_ : c_oid, PK, not null
        * creation_date_ : timestamp
        * last_access_date_ : timestamp
        * lease_time_ : int4
        * ip_addr_ : cidr
        * user_ : c_oid, not null, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Session, self ).__init__( db, **kwargs )


    def new(self, user, key):
        # crée un nouveau jeton
        self.key_.value = key
        self.last_access_date_.value = datetime.now()
        self._user_ = user
        self.insert()

    @property
    def user(self):
        return self._user_
