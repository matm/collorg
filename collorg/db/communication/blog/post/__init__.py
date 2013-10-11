#-*- coding: UTF-8 -*-

from datetime import datetime
from collorg.db.core.base_table import Base_table
from collorg.utils.mail import Mail
from collorg.templates.document_type.html import Html

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
    __is_cog_post = True
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

    @property
    def is_cog_post(self):
        return self.__is_cog_post

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
        tag_t.tag_.set_intention(tag)
        if not tag_t.exists():
            tag_t.insert()
        atp = self._rev_a_tag_post_
        order = atp.count() + 1
        atp.tag_.set_intention(tag)
        if not atp.exists():
            atp.data_type_.set_intention(ref_data.fqtn)
            atp.order_.set_intention(order)
            atp.status_.set_intention(status)
            atp.insert()

    def del_tag(self, tag, ref_data = None, status = None):
        """
        The tag is removed if it's not referenced.
        if @status is specified, a_tag_post must have this status for the
        tag to be removed.
        """
        atp = self._rev_a_tag_post_
        atp.tag_.set_intention(tag)
        atp.data_type_.set_intention(ref_data.fqtn)
        atp.status_.set_intention(status)
        if atp.count() == 1:
            atp.delete()
            tag_t = self.db.table('collorg.communication.tag')
            tag_t.tag_.set_intention(tag)
            if not tag_t._rev_a_tag_post_.exists():
                tag_t.delete()

    def has_tag(self, tag):
        atp = self._rev_a_tag_post_
        atp.data_type_.set_not_null()
        atp.tag_.set_intention(tag)
        return atp.exists()

    def is_owned_by(self, user):
        if user is None:
            return False
        owner = self._author_.get()
        return owner.cog_oid_.value == user.cog_oid_.value

    def wupdate(self, n_elt = None, **kwargs):
        """
        update a post. Invoked by template w3save
        """
        n_post = n_elt or self()
        n_post.title_.set_intention(kwargs['title_'].strip() or None)
        n_post.introductory_paragraph_.set_intention(
            kwargs.get('introductory_paragraph_'))
        n_post.text_.set_intention(kwargs['text_'].strip() or None)
        n_post.public_.set_intention(kwargs.get('public_', False))
        n_post.comment_.set_intention(kwargs.get('comment_', False))
        n_post.visibility_.set_intention(kwargs.get('visibility_', None))
        expiry_date = kwargs.get('expiry_date_')
        if expiry_date:
            n_post.expiry_date_.set_intention(expiry_date)
        else:
            n_post.expiry_date_.set_null()
        self.update(n_post)
        tag = self.db.table('collorg.communication.tag')
        tag.wsave(data=self, tags=kwargs.get('tag_', ''))
        return self

    def link_to_data(self, data):
        """
        data must be a topic or a post
        """
        self.get()
        apd = self._rev_a_post_data_post_
        apd._data_ = data
        apd._who_ = self._cog_controller.user
        apd.insert()
        return self

    def unlink_from_data(self, data):
        #untested (this is a joke). Never used yet...
        self.get()
        apd = self._rev_a_post_data_post_
        apd._data_ = data
        apd.delete()
        return self

    def move(self, from_, to_):
        apd = self._rev_a_post_data_post_
        apd._data_ = from_
        napd = apd()
        napd._data_ = to_
        apd.update(napd)

    def winsert(self, user, **kwargs):
        data_oid = kwargs['data_oid']
        data = kwargs.get('data', self.db.get_elt_by_oid(data_oid))
        data_fqtns = [data.fqtn] + data.parents_fqtns()
        if (not 'collorg.web.topic' in data_fqtns and
            not 'collorg.communication.blog.post' in data_fqtns):
                data = data.get_root_topic().get()
        tag = self.db.table('collorg.communication.tag')
        self.title_.set_intention(kwargs['title_'].strip() or None)
        self.text_.set_intention(kwargs['text_'].strip() or None)
        ip = kwargs.get('introductory_paragraph_')
        if ip is not None:
            ip = ip.strip() or None
        self.introductory_paragraph_.set_intention(ip)
        self.public_.set_intention(kwargs.get('public_', None))
        self.comment_.set_intention(kwargs.get('comment_', None))
        self.important_.set_intention(kwargs.get('important_'))
        self.visibility_.set_intention(kwargs['visibility_'])
        self.author_.set_intention(user.cog_oid_.value)
        self = self.insert()
        data_oid and self.link_to_data(data)
        access = self.db.table('collorg.access.access')
        function = self.db.table('collorg.actor.function')
        function.long_name_.set_intention('Collorg actor')
        access.grant(user=user, function=function, data=self, write=True)
        tag = self.db.table('collorg.communication.tag')
        tag.wsave(data=self, tags=kwargs.get('tag_', ''))
        if kwargs.get('email'):
            self.mail()
        return self

    def wdelete(self):
        assert self.count() == 1
        access = self._rev_access_
        access._rev_role_.delete()
        access.delete()
        self._rev_a_post_data_post_.delete()
        self._rev_see_also_post_.delete()
        self._rev_a_tag_post_.delete()
        group = self.db.table('collorg.group.group')
        group._data_ = self
        topic = self.db.table('collorg.web.topic')
        topic._cog_environment_ = group
        print(topic.count())
        topic.delete()
        group._rev_calendar_.delete()
        group.delete()
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
        exp = self._cog_controller.user.email_.value
        recipient = self.db.get_elt_by_oid(kwargs['recipient_oid']).members
        mail = Mail(self.db)
        mail.set_from(exp)
#        mail.set_to([exp])
        mail.set_to([elt.email_.value for elt in recipient]) # was bcc
        self.set_mail_subject(mail, kwargs.get('title_'))
        self.set_mail_body(mail, kwargs.get('text_'))
        mail.send()

    def get_post_types(self):
        if Post.__post_types is None:
            Post.__post_types = []
            for fqtn in self.db.fqtns:
                obj = self.db.table(fqtn)
                if hasattr(obj, '_Post__is_cog_post'):
                    Post.__post_types.append(obj)
        return Post.__post_types

    def add_see_also(self, **kwargs):
        sa = self._rev_see_also_post_
        data = self.db.get_elt_by_oid(kwargs['data_oid'])
        if data.cog_fqtn_.value == 'collorg.web.topic':
            data.set_parent(self, link = True)
        else:
            sa._data_ = data
            if not sa.exists():
                sa.insert()

    def delete_see_also(self, data):
        sa = self._rev_see_also_post_
        sa._data_ = data
        assert sa.count() == 1
        sa.delete()

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
        follow_up.text_.set_intention(kwargs['text_'])
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
        user_check.communication_object_.set_intention(comment.cog_oid_.value)
        if user:
            user_check.user_.set_intention(user.cog_oid_.value)
        if not poll:
            user_check.delete()
        user_check = user_check()
        user_check.communication_object_.set_intention(comment.cog_oid_.value)
        user_check.user_.set_intention(self._cog_controller.user.cog_oid_)
        user_check.date_checked_.set_intention(datetime.now())
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

    def get_children(self):
        tg = self._rev_topic_graph_()
        tg._parent_ = self
        return tg._topic_

    def get_accessible_children(self, user):
        return self.get_children()
        topics = self.get_not_private_children()
        topics += self.get_private_children(user)
        return topics

    def get_not_private_children(self):
        topics = self.get_children()
        topics.visibility_.set_intention('private', '!=')
        return topics

    def get_private_children(self, user):
        """
        Returns private children topics of self
        """
        priv_posts = self.db.table('collorg.web.topic')
        priv_posts.cog_oid_.set_intention(
            self._rev_a_post_data_data_._post_.cog_oid_)
        priv_posts.visibility_.set_intention('private')
        accessible_posts = user.get_granted_data()
        priv_posts.cog_oid_ *= accessible_posts.cog_oid_
        return priv_posts

    def get_see_also(self):
        """
        returns None if no see_also.
        otherwise returns the set of posts attach to self.
        """
        apd = self.db.table('collorg.communication.blog.a_post_data')
        apd._data_ = self
        see_also = self()
        see_also.cog_oid_.set_null()
        if apd.exists() or self._rev_see_also_post_._data_.exists():
            data = self._rev_see_also_post_._data_
            see_also = self.db.table('collorg.communication.blog.post')
            see_also.cog_oid_.set_intention(data.cog_oid_)
            see_also.cog_fqtn_.set_intention('collorg.web.topic', '!=')
            if apd.exists():
                sub_posts = self.db.table('collorg.communication.blog.post')
                sub_posts.cog_oid_.set_intention(apd._post_.cog_oid_)
                sub_posts.cog_fqtn_.set_intention('collorg.web.topic', '!=')
                see_also += sub_posts
            see_also.visibility_.set_intention('private', '!=')
            user = self._cog_controller.user
            if user:
                p_see_also = see_also()
                p_see_also.cog_oid_.set_intention(data.cog_oid_)
                p_see_also.cog_fqtn_.set_intention('collorg.web.topic', '!=')
                see_also += (p_see_also * user.get_granted_data())
        return see_also
