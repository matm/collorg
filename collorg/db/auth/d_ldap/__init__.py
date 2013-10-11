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

class LdapWrongDomainError(Exception): pass
class LdapDefaultDomainError(Exception): pass

try:
    import ldap as ldap_module
except:
    pass

class D_ldap( Base_table ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.auth'
    _cog_tablename = 'd_ldap'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _connectivity_security_ = cog_r._connectivity_security_
    _certificate_checks_ = cog_r._certificate_checks_
    _scope_ = cog_r._scope_
    # REVERSE
    _rev_user_ = cog_r._rev_user_
    #<<< AUTO_COG REL_PART. Your code goes after
    __default_domain = None
    __domains = {}
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
        * domain_ : string, PK, not null
        * host_ : string, uniq, not null
        * port_ : int2
        * account_ : string
        * password_ : password
        * connectivity_security_ : c_oid, FK
        * certificate_checks_ : c_oid, FK
        * base_dn_ : string, uniq, not null
        * organizational_unit_ : string, not null
        * filter_ : string, uniq
        * scope_ : c_oid, FK
        * login_attr_ : string, not null
        * first_name_attr_ : string
        * last_name_attr_ : string
        * e_mail_attr_ : string
        * default_ : bool
        """
        #<<< AUTO_COG DOC. Your code goes after
        self.con = None
        self._base_dn = None
        super( D_ldap, self ).__init__( db, **kwargs )

    def load_domains(self):
        """
        can be invoked to reload all the domains
        """
        D_ldap.__domains = {}
        D_ldap.__default_domain = None
        for dom in self.get_extent():
            dom_name = dom.domain_.val
            D_ldap.__domains[dom_name] = {}
            for field in dom._cog_fields:
                fname = field.pyname
                D_ldap.__domains[dom_name][fname] = dom.__dict__[fname].val
            if dom.default_.val:
                D_ldap.__default_domain = dom.domain_.val

    def get_default_domain(self):
        if not self.__domains:
            self.load_domains()
        return self.__default_domain

    def get_domain(self, domain):
        if not domain in self.__ldap: raise LdapWrongDomainError
        return self.__ldap[domain]

    def auth(self, login, password, domain):
        """
        very basic authentication. No ssl
        """
        if domain == '':
            domain = self.get_default_domain()
        self.domain = self.__domains[domain]
        #XXX diff between LDAPS and START_TLS?
        ssl = self.domain['connectivity_security_'] or ""
        port = self.domain['port_']
        if not port:
            if ssl: port = 636
            else: port = 389
        self.ldap_url = "ldap%s://%s:%s/" % (
            ssl and "s", self.domain['host_'], port)
        self.con = ldap_module.initialize(self.ldap_url)
        self.con.protocol_version = ldap_module.VERSION3
        ou_ = ""
        if self.domain['organizational_unit_']:
            ou_ = "ou=%s," % (self.domain['organizational_unit_'])
        self._base_dn = "%s%s" % (ou_, self.domain['base_dn_'])
        self._filter = "%s=%s" % (self.domain['login_attr_'], login)
        self.ldap_dn = "%s,%s" % (self._filter, self._base_dn)
        if 1:#try:
            self.con.simple_bind(self.ldap_dn, password)
            whoami = self.con.whoami_s()
            user_info = False
            self.con.unbind()
            if whoami == 'dn:%s' % (self.ldap_dn):
                user_info = self.__retreive_user_info()
            self.con.unbind()
            return user_info, self.domain
        else:#except:
            return False, False

    def __retreive_user_info(self):
        assert self._filter
        self.con = ldap_module.initialize(self.ldap_url)
        self.search_scope = getattr(ldap_module, 'SCOPE_SUBTREE')
        ldap_result_id = self.con.search(
            self.domain['base_dn_'], self.search_scope, self._filter, None)
        result_type, result_data = self.con.result(ldap_result_id)
        for result in result_data:
            if result[0] == self.ldap_dn:
                return result[1]
