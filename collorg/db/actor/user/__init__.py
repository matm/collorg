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

from time import sleep
from collorg.db.actor.actor import Actor
from collorg.db.group._groupable import Groupable
import uuid
import hashlib

try:
    import ldap
    ldap_ = True
except:
    ldap_ = False

class NoPasswdError(Exception): pass
class ToManyAccountError(Exception): pass
class SessionKeyError(Exception): pass

class User(Actor, Groupable):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.actor'
    _cog_tablename = 'user'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _ldap_ = cog_r._ldap_
    _photo_ = cog_r._photo_
    # REVERSE
    _rev_a_user_category_ = cog_r._rev_a_user_category_
    _rev_post_ = cog_r._rev_post_
    _rev_log_ = cog_r._rev_log_
    _rev_user_check_ = cog_r._rev_user_check_
    _rev_topic_ = cog_r._rev_topic_
    _rev_access_ = cog_r._rev_access_
    _rev_bookmark_ = cog_r._rev_bookmark_
    _rev_attachment_ = cog_r._rev_attachment_
    _rev_file_ = cog_r._rev_file_
    _rev_session_ = cog_r._rev_session_
    _rev_follow_up_ = cog_r._rev_follow_up_
    _rev_relation_me_ = cog_r._rev_relation_me_
    _rev_relation_my_relation_ = cog_r._rev_relation_my_relation_
    _rev_comment_ = cog_r._rev_comment_
    _rev_a_post_data_ = cog_r._rev_a_post_data_
    #<<< AUTO_COG REL_PART. Your code goes after
    _is_cog_user = True
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
        * first_name_ : string, not null
        * last_name_ : string, not null
        * gender_ : bpchar
        * birthday_ : date
        * email_ : email, PK, not null
        * pseudo_ : text, uniq
        * password_ : password, not null
        * validation_key_ : c_oid, not null
        * valid_account_ : bool
        * system_account_ : bool
        * ldap_ : c_oid, FK
        * photo_ : c_oid, FK
        * url_ : url
        """
        #<<< AUTO_COG DOC. Your code goes after
        self.__groups = None
        super(User, self).__init__(db, **kwargs)

    @property
    def cog_session_key(self):
        assert self.cog_oid_.value
        return self.db._cog_controller._session.key_

    @property
    def cog_group_name(self):
        return "%s %s's private group" % (self.first_name_, self.last_name_)

    @property
    def _cog_label(self):
        return ["{} {}", self.first_name_, self.last_name_]

    def is_(self, user):
        if user is None:
            return False
        return self.cog_oid_.value == user.cog_oid_.value

    def __grant_self_access(self):
        #XXX les tests sont là pour le cas ou des créations partielles sont
        #    encore présentes... À supprimer
        access = self._rev_access_
        function = self.db.table('collorg.actor.function')
        function.name_.set_intention('Collorg actor')
        access = self.db.table('collorg.access.access')
        access.grant(user=self, data=self, function=function)

    def new_account(self, **kwargs):
        self.db.set_auto_commit(False)
        new = self()
        new.email_.set_intention(kwargs['email_'] or None)
        if new.exists():
            raise RuntimeError("an account already exists for this email")
        new.pseudo_.set_intention(kwargs.get('pseudo_', None))
        new.first_name_.set_intention(kwargs['first_name_'] or " ")
        new.last_name_.set_intention(kwargs['last_name_'] or " ")
        new.ldap_.set_intention(kwargs.get('ldap_', None))
        password = kwargs.get('password_', uuid.uuid4())
        salt = uuid.uuid4()
        salted_password = "%s%s" % (salt, password)
        new.password_.set_intention(
            hashlib.sha256(salted_password.encode('utf-8')).hexdigest())
        new.validation_key_.set_intention(salt)
        new.insert()
        topic = new._rev_topic_
        topic.title_.set_intention('')
        topic.text_.set_intention('')
        topic.path_info_.set_intention('')
        topic.author_.set_intention(new.cog_oid_)
        topic.cog_environment_.set_intention(new.cog_oid_)
        topic.insert()
        new.grant_access(new, True)
        new.grant_access(topic, True)
        self.db.commit()
        return new

    def root_topic(self):
        topic = self._rev_topic_
        topic.path_info_.set_intention('')
        topic.cog_environment_.set_intention(self.cog_oid_)
        return topic

    def remove_account(self):
        """
        Removes the account and all contributions
        """
        self._rev_access_.delete()
        self._rev_a_user_category_.delete()
        self._rev_comment_.delete()
        self._rev_post_.delete()
        self.delete()

    def login(self, login, password, domain):
        """
        returns the key of the session (None on failure)
        """
        auth_result = self.__authentication(login, password, domain)
        if auth_result:
            cog_session = self._cog_controller.set_cookie('cog_session')
            self.__grant_self_access()
            session = self.db.table('collorg.web.session')
            session.new(self, cog_session)
            self._cog_controller.set_user(self.cog_oid_.value)
            return cog_session
        return auth_result

    def logout(self):
        sess = self._rev_session_
        key = self._cog_controller.get_cookie('cog_session')
        self._cog_controller.delete_cookie('cog_session')
        self._cog_controller._user = None
        if key is not None:
            sess.key_.set_intention(key)
            if sess.exists():
                sess.delete()
                self._cog_controller.del_user(key)
            f_ = self.db.table('collorg.communication.file')
            f_.remove_session_repos(key)
#                self._cog_controller.set_user()
        site = self._cog_controller.load_site()
        home_site_link = ""
        cart_msg = self._cog_controller.i18n.gettext(
            'Drop your links here<br>for future reference')
        reset_cart = ('<li class="placeholder rotate">{}.</li></ul>').format(
            cart_msg)
        site._cog_controller.add_json_res({
            '#cog_log_link':self.w3login_link(),
            '#cog_home_link':home_site_link,
            '#cog_session':self._cog_controller.new_session,
            '#cog_cart ul':reset_cart,
            '#cog_user_actions':'',
            '#cog_container':site.w3display(cog_first_call = True)})

    def __authentication(self, login, password, domain):
        if not password:
            return False
        if login.find('@') != -1:
            self.email_.set_intention(login.strip())
        else:
            self.pseudo_.set_intention(login.strip())
        if not self.count() <= 1: raise ToManyAccountError
        if self.count():
            self.get()
            login = self.pseudo_.val
            if self.ldap_.val is None:
                return self.__db_auth(password)
        # we check for an ldap account even if it's not yet in the db
        if ldap_:
            try:
                user_info, domain = self.__ldap_auth(login, password, domain)
            except:
                return False
            if user_info and not self.exists():
                new = self.new_account(
                    pseudo_ = login,
                    first_name_ = user_info[domain['first_name_attr_']][0],
                    last_name_ = user_info[domain['last_name_attr_']][0],
                    email_ = user_info[domain['e_mail_attr_']][0].lower(),
                    ldap_ = domain['cog_oid_'])
                self.cog_oid_.set_intention(new.cog_oid_.val)
            return user_info and True

    def __db_auth(self, password):
        this = self.get()
        salted_password = "%s%s" % (this.validation_key_, password)
        c_p = hashlib.sha256(salted_password.encode('utf-8')).hexdigest()
        return c_p == this.password_

    def __ldap_auth(self, login, password, domain):
        return self.db.table('collorg.auth.d_ldap').auth(
            login, password, domain)

    def is_valid(self):
        return self.get().valid_account_ == True

    def valid_account(self, validation_key):
        self = self.get()
        assert self.validation_key_ == validation_key
        n_self = self()
        n_self.valid_account_.set_intention(True)
        return self.update(n_self)

    def is_member(self, data):
        return (data.members * self).count() > 0

    def has_access(self, data, write = None):
        data_base = self.db.table('collorg.core.base_table')
        data_base.cog_oid_.set_intention(data.cog_oid_)
        data_env = data_base()
        access = self.db.table('collorg.access.access')
        access._user_ = self
        data_env.cog_oid_.set_intention(data_base.cog_environment_)
        access.data_.set_intention(data.cog_oid_)
        access.data_ += (data_env.cog_oid_, '=')
        if write:
            access.write_.set_intention(write)
        return access.is_granted()

    def get_granted_data(self, fqtn = None):
        data = self._rev_access_.granted()._data_
        if fqtn:
            data.cog_restrict_to_type(fqtn)
        return data

    def has_function(self, function_long_name):
        """
        Has the function if has a role granted...
        """
        assert self.count() == 1
        function = self.db.function(
            'collorg.actor.function', long_name_ = function_long_name)
        role = function._rev_role_
        access = self._rev_access_
        access.granted()
        role *= access._rev_role_
        return role.is_granted()

    def grant_access(
        self, data, write = False, function_long_name = None,
        begin_date = None, end_date = None, pourcentage = None):
        access = self._rev_access_
        access._data_ = data
        if function_long_name is not None:
            function = self.db.table('collorg.actor.function')
            function.long_name_.set_intention(function_long_name)
            access._function_ = function
        access.grant(
            self, write = write,
            begin_date = begin_date, end_date = end_date,
            pourcentage = pourcentage)
        sleep(0.5)

    def revoke_access(self, data):
        access = self._rev_access_
        access._data_ = data
        access.revoke()

    def revoke_write_access(self, data):
        access = self._rev_access_
        access._data_ = data
        access.revoke_write()

    def grant_write_access(self, data):
        access = self._rev_access_
        access._data_ = data
        access.grant_write()
