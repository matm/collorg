#-*- coding: utf-8 -*-

import os
import shutil
import qrcode

from time import sleep
from datetime import datetime
from collorg.db.core.base_table import Base_table
from collorg.utils.mail import Mail
from collorg.templates.document_type.html import Html
from functools import wraps

def wipe_cache(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        self._wipe_cache()
        return function(self, *args, **kwargs)
    return wrapper

class Post(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication.blog'
    _cog_tablename = 'post'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _author_ = cog_r._author_
    #<<< AUTO_COG REL_PART. Your code goes after
    _is_of_type_post = True
    _is_cog_post = True
    __post_types = None
    __cog_type_name = 'Post'
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
        * title_ : string, not null
        * introductory_paragraph_ : string
        * text_ : wiki, not null
        * author_ : c_oid, not null, FK
        * public_ : bool
        * comment_ : bool
        * expiry_date_ : timestamp
        * important_ : bool
        * broadcast_ : bool
        * visibility_ : string, not null
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Post, self).__init__(db, **kwargs)
        self.__cache_path = ''

    @property
    def is_cog_post(self):
        return self._is_cog_post

    @property
    def _cog_label(self):
        return ["{}", self.title_]

    def add_tag(self, tag, ref_data = None, status = None):
        """
        @ref_data: used to store ref_data.fqtn with the a_tag_post
        association.
        @status: the status associated with a_tag_post
        """
        tag_t = self.db.table('collorg.communication.tag')
        tag_t.tag_.value = tag
        if tag_t.is_empty():
            tag_t.insert()
        atp = self._rev_a_tag_post_
        order = atp.count() + 1
        atp.tag_.value = tag
        if atp.is_empty():
            atp.data_type_.value = ref_data.fqtn
            atp.order_.value = order
            atp.status_.value = status
            atp.insert()

    def del_tag(self, tag, ref_data = None, status = None):
        """
        The tag is removed if it's not referenced.
        if @status is specified, a_tag_post must have this status for the
        tag to be removed.
        """
        atp = self._rev_a_tag_post_
        atp.tag_.value = tag
        atp.data_type_.value = ref_data.fqtn
        atp.status_.value = status
        if atp.count() == 1:
            atp.delete()
            tag_t = self.db.table('collorg.communication.tag')
            tag_t.tag_.value = tag
            if tag_t._rev_a_tag_post_.is_empty():
                tag_t.delete()

    def has_tag(self, tag):
        atp = self._rev_a_tag_post_
        atp.data_type_.set_not_null()
        atp.tag_.value = tag
        return not atp.is_empty()

    def is_owned_by(self, user):
        if user is None:
            return False
        owner = self._author_.get()
        return owner.cog_oid_.value == user.cog_oid_.value

    def link_to_data(self, data):
        """
        data must be a topic or a post
        """
        self.get()
        apd = data._rev_a_post_data_data_
        apd._post_ = self
        apd._who_ = self._cog_controller.user
        apd.insert()
        apd.get()
        data._wipe_cache()
        return self

    def unlink_from_data(self, data):
        #untested (this is a joke). Never used yet...
        self.get()
        apd = self._rev_a_post_data_post_
        apd._data_ = data
        apd.delete()
        data._wipe_cache()
        return self

    def move(self, from_, to_):
        apd = self._rev_a_post_data_post_
        apd._data_ = from_
        napd = apd()
        napd._data_ = to_
        apd.update(napd)

    def winsert(self, user, grant_access=True, **kwargs):
        """
        data_oid
        title_
        text_
        introductory_paragraph_
        public_
        comment_
        important_
        visibility_
        function_oid
        """
        data_oid = kwargs['data_oid']
        data = kwargs.get('data', self.db.get_elt_by_oid(data_oid))
        data_fqtns = [data.fqtn] + data.parents_fqtns()
        if (not 'collorg.web.topic' in data_fqtns and
            not 'collorg.communication.blog.post' in data_fqtns):
                try:
                    data = data.get_root_topic().get()
                except:
                    # groups, ...
                    pass
        self.title_.value = kwargs['title_'].strip() or None
        self.text_.value = kwargs['text_'].strip() or None
        ip = kwargs.get('introductory_paragraph_')
        if ip is not None:
            ip = ip.strip() or None
        self.introductory_paragraph_.value = ip
        self.public_.value = kwargs.get('public_', None)
        self.comment_.value = kwargs.get('comment_', None)
        self.important_.value = kwargs.get('important_')
        self.visibility_.value = kwargs['visibility_']
        self.author_.value = user.cog_oid_.value
        self = self.insert()
        data_oid and self.link_to_data(data)
        function_oid = kwargs.get('function_oid')
        function = None
        if function_oid:
            function = self.db.get_elt_by_oid(function_oid)
        if grant_access:
            user.grant_access(self, function=function, write=True)
        tag = self.db.table('collorg.communication.tag')
        tag.wsave(data=self, tags=kwargs.get('tag_', ''))
        if kwargs.get('email'):
            self.mail()
        sleep(0.5) #XXX insert
        self.get().w3display()
        self._wipe_cache()
        return self

    def wupdate(self, n_elt = None, **kwargs):
        """
        update a post. Invoked by template w3save
        """
        n_post = n_elt or self()
        n_post.title_.value = kwargs['title_'].strip() or None
        n_post.introductory_paragraph_.value = \
            kwargs.get('introductory_paragraph_')
        n_post.text_.value = kwargs['text_'].strip() or None
        n_post.public_.value = kwargs.get('public_', False)
        n_post.comment_.value = kwargs.get('comment_', False)
        n_post.visibility_.value = kwargs.get('visibility_', None)
        expiry_date = kwargs.get('expiry_date_')
        if expiry_date:
            n_post.expiry_date_.value = expiry_date
        else:
            n_post.expiry_date_.set_null()
        self.update(n_post)
        tag = self.db.table('collorg.communication.tag')
        tag.wsave(data=self, tags=kwargs.get('tag_', ''))
        new = self()
        new.cog_oid_.value = self.cog_oid_.value
        new.get()
        new._wipe_cache()
        return new

    def wdelete(self):
        assert self.count() == 1
        access = self._rev_access_
        access._rev_role_.delete()
        access.delete()
        self._rev_a_post_data_post_.delete()
        self._rev_a_tag_post_.delete()
        group = self.db.table('collorg.group.group')
        group._data_ = self
        topic = self.db.table('collorg.web.topic')
        topic._cog_environment_ = group
        print(topic.count())
        topic.delete()
        group._rev_calendar_.delete()
        group.delete()
        self._wipe_cache()
        self.delete()

    def set_mail_subject(self, mail, subject = None):
        mail.set_subject(unicode("{} {}".format(
            self.db._cog_params['mail_prefix'],
            subject or self.title_.value), 'utf-8') or "")

    def set_mail_body(self, mail, body = ''):
        html = Html(self)
        self_link = html.absolute_link()
        html_body = "{}<hr>{}{}".format(
            html.creole(body), self_link,
            html().display(self.text_, label=''))
        mail.set_body(body + self.text_.value)
        mail.set_body(html_body, 'html')

    def mail(self, **kwargs):
        sender = self._cog_controller.user.email_.value
        recipients = self.relation('collorg.actor.user')
        recipients.cog_oid_.value = kwargs['recipient_oid']
        emails = [sender]
        for elt in recipients:
            email = elt.email_.value
            if not email in emails:
                emails.append(email)
        other_recipient = kwargs.get('other_recipient', [])
        other_emails = [elt.strip() for elt in other_recipient.split(',')]
        emails += other_emails
        mail = Mail(self.db)
        mail.set_from(sender)
        mail.set_to(emails)
        self.set_mail_subject(mail, kwargs.get('title_'))
        self.set_mail_body(mail, kwargs.get('text_'))
        mail.send()

    def get_post_types(self):
        if Post.__post_types is None:
            Post.__post_types = []
            for fqtn in self.db.fqtns:
                obj = self.db.table(fqtn)
                if hasattr(obj, '_is_cog_post'):
                    Post.__post_types.append(obj)
        return Post.__post_types

    def add_see_also(self, **kwargs):
        apd = self._rev_a_post_data_data_
        post = self.db.get_elt_by_oid(kwargs['data_oid'])
        apd._post_ = post
        if apd.is_empty():
            apd.see_also_.value = True
            apd.insert()

    def attach_comment(self, comment):
        assert self.comment_.value
        comment._data_ = self
        comment._author_ = self._cog_controller.user
        comment.insert()
        self._check_comment(comment)
        return comment

    def attach_follow_up(self, **kwargs):
        comment_oid = kwargs['comment_oid']
        comment = self.db.get_elt_by_oid(comment_oid)
        follow_up = comment._rev_follow_up_
        follow_up.text_.value = kwargs['text_']
        assert self.comment_.value
        assert self.cog_oid_.value == comment._data_.get().cog_oid_.value
        self.db.set_auto_commit(False)
        self._check_comment(comment)
        comment.attach_follow_up(follow_up)
        self.db.commit()

    def _check_comment(self, comment, user = None, poll = False):
        """
        On follow_up, the comment is tagged check with the now date. Il
        it's the first the comment is checked, the tuple is inserted,
        otherwise it's updated.
        If poll is set to True, the check tuple is always inserted to
        garantee the user votes only once.
        """
        assert comment.cog_oid_.value
        user_check = self.db.table('collorg.communication.user_check')
        user_check.communication_object_.value = comment.cog_oid_.value
        if user:
            user_check.user_.value = user.cog_oid_.value
        if not poll:
            user_check.delete()
        user_check = user_check()
        user_check.communication_object_.value = comment.cog_oid_.value
        user_check.user_.value = self._cog_controller.user.cog_oid_
        user_check.date_checked_.value = datetime.now()
        user_check.insert()

    def check_visibility(self, cog_user):
        visibility = self.visibility_.value
        if visibility == 'public':
            return True
        if cog_user is None:
            return False
        if visibility == 'protected':
            return True
        if visibility == 'private':
            return cog_user.has_access(self)
        return False

    def get_see_also(self):
        """
        returns the set of posts attach to self.
        """
        apd = self.db.table('collorg.communication.blog.a_post_data')
        apd._data_ = self
        see_also = self()
        see_also.cog_oid_.set_null()
        if not apd.is_empty():
            see_also.cog_oid_.value = apd._post_.cog_oid_
            user = self._cog_controller.user
            if user:
                p_see_also = see_also()
                p_see_also.cog_oid_.value = apd._post_.cog_oid_
                see_also += p_see_also * user.get_granted_data()
            else:
                pub_see_also = see_also()
                pub_see_also.visibility_.value = 'private', '!='
                see_also *= pub_see_also
        return see_also

    def get_children(self):
        children = self.db.table('collorg.communication.blog.view.children')
        children.parent_oid_.value = self.cog_oid_.value
        children.cog_fqtn_.value = 'collorg.web.topic'
        return children

    def get_accessible_children(self, user):
        if not user:
            children = self.__get_not_private_children()
        else:
            children = self.__get_not_private_children() + \
                self.__get_private_children(user)
        children.order_by(children.order_)
        return children

    def __get_not_private_children(self):
        children = self.get_children()
        children.visibility_.value = 'private', '!='
        return children

    def __get_private_children(self, user):
        """
        Returns private children topics of self
        """
        children = self.get_children()
        accessible_posts = user.get_granted_data()
        children *= accessible_posts
        return children

    def sort_attached_posts(self, elt_, prev_, next_):
        """
        Sort the attached posts.
        elt_ is the moved element. It's just been moved between prev_ and
        next_.
        We renumber all a_post_data with data = self and post not of
        type 'collorg.web.topic'.
        """
        apd_elt = self._rev_a_post_data_data_
        apd_elt._post_ = elt_
        if next_:
            #  We increment by 1 everything from next_
            apd_next = self._rev_a_post_data_data_
            apd_next._post_ = next_
            next_position = apd_next.get().order_.value
            apd = self._rev_a_post_data_data_
            apd.order_.value = next_position, '>='
            apd.increment(apd.order_)
            apd = self._rev_a_post_data_data_
            apd._post_ = elt_
            napd = apd()
            napd.order_.value = next_position
            apd.update(napd)
        else:
            apd = self._rev_a_post_data_data_
            napd = apd()
            max_order = apd.max(apd.order_) or 0
            napd.order_.value = max_order + 1
            apd_elt.update(napd)
        self._wipe_cache()

    @property
    def _cache_path(self):
        if not self.__cache_path:
            self.__cache_path = '{}/{}/{}/{}'.format(
                self.db._cog_params['cache_path'],
                self.cog_oid_.value[0:2], self.cog_oid_.value[2:4],
                self.cog_oid_)
        return self.__cache_path

    def _wipe_cache(self, deja_vus = None):
        """
        The cache is wiped when there is a modification. It'll be re-generated
        at first none connected access.
        """
        if deja_vus is None:
            deja_vus = []
        for elt in self:
            cog_oid = elt.cog_oid_.value
            if cog_oid in deja_vus:
                continue
            deja_vus.append(cog_oid)
            if os.path.exists(elt._cache_path):
                shutil.rmtree(elt._cache_path)
            data = self()
            data.cog_oid_.value = \
                elt._rev_a_post_data_post_._data_.cog_oid_
            deja_vu = self()
            deja_vu.cog_oid_.value = deja_vus
            data -= deja_vu
            data._wipe_cache(deja_vus)

    def _cog_get_cache(self, func_name):
        assert (func_name == 'w3display' and self._is_cog_post and
            self.visibility_.value == 'public')
        if self.fqtn == 'collorg.web.topic' and self.data_type_.value:
            return None
        if not os.path.exists(self._cache_path):
            os.makedirs(self._cache_path)
        file_ = "{}/w3display".format(self._cache_path)
        if not os.path.exists(file_):
            open(file_, 'w').write(str(self.w3display(no_cog_user=True)))
        if os.path.exists(self._cache_path):
            return open('{}/{}'.format(
                self._cache_path, func_name)).read()
        return None
