#-*- coding: utf-8 -*-

from collorg.db.communication.blog.post import Post

class Topic(Post):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.web'
    _cog_tablename = 'topic'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # DIRECT
    _data_type_ = cog_r._data_type_
    _post_type_ = cog_r._post_type_
    _action_ = cog_r._action_
    _author_ = cog_r._author_
    _site_ = cog_r._site_
    # REVERSE
    _rev_a_rss_topic_ = cog_r._rev_a_rss_topic_
    _rev_wall_topic_ = cog_r._rev_wall_topic_
    _rev_wall_parent_ = cog_r._rev_wall_parent_
    _rev_a_topic_function_ = cog_r._rev_a_topic_function_
    #<<< AUTO_COG REL_PART. Your code goes after
    __cog_type_name = 'Folder'
    _is_cog_folder = True
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
        * cog_environment_ : c_oid, inherited, PK, not null
        * cog_state_ : text, inherited
        * title_ : string, inherited, not null
        * introductory_paragraph_ : string
        * text_ : wiki, inherited, not null
        * author_ : c_oid, inherited, not null, FK
        * public_ : bool, inherited
        * comment_ : bool, inherited
        * expiry_date_ : timestamp, inherited
        * important_ : bool, inherited
        * broadcast_ : bool, inherited
        * visibility_ : string, inherited, not null
        * path_info_ : string, PK, not null
        * site_ : c_oid, FK
        * data_type_ : c_fqtn, FK
        * action_ : c_oid, FK
        * post_type_ : c_fqtn, FK
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Topic, self).__init__(db, **kwargs)

    def cog_ref_obj(self):
        return [self._cog_environment_]

    @property
    def _cog_label(self):
        image = "folder.png"
        if self.visibility_.value == 'protected':
            image = "protected_folder.png"
        if self.visibility_.value == 'private':
            image = "private_folder.png"
        label = self.title_.value
        if not label and self.cog_oid_.value != self.cog_environment_.value:
            label = self._cog_environment_.get().cog_label()
        if not label:
            label = "No label"
        label = ('<img style="display:inline-block;" ' +
            'src="/collorg/images/{}" ' +
            'alt="Folder" /> {}').format(image, label)
        return [label]

    def __get_parent(self):
        tg = self.db.table('collorg.communication.blog.a_post_data')
        tg._post_ = self
        tg.see_also_.value = False
        parent = tg._data_
        if not parent.is_empty():
            return parent.get() # 1 and only 1 parent
        return None

    def get_parents(self):
        parents = []
        parent = self.__get_parent()
        while parent:
            parents.append(parent)
            if parent.cog_fqtn_.value == 'collorg.web.topic':
                parent = parent.__get_parent()
            else:
                break
        return parents

    def set_root(self, obj, author):
        assert obj.cog_oid_.value
        self.cog_environment_.value = obj.cog_oid_
        self.path_info_.value = ''
        self.title_.value = obj.cog_label()
        self._author_ = author
        assert self.is_empty()
        self.insert()

    def get_root(self, obj):
        site = self._cog_controller.site
        self.site_.value = site.cog_oid_.value
        self.cog_environment_.value = obj.cog_oid_
        if not self.is_empty():
            self.order_by(self.path_info_)
            self.cog_limit(1)
            return self.get()
        self = self()
        self.cog_environment_.value = obj.cog_oid_
        self.path_info_.value = ''
        return self

    def link_to(self, parent):
        tg = self._rev_a_post_data_post_
        tg._data_ = parent
        tg.insert()

    def __get_rel_path_info(self):
        raise NotImplementedError
        return self.path_info_.value.split("/")[-1:][0]

    def insert_in(self, parent, sub_path_info):
        self._site_ = parent._site_
        if not self.is_empty():
            raise ValueError("Topic already present for this site")
        self.path_info_.value = "{}/{}".format(parent.path_info_, sub_path_info)
        if self.is_empty():
            self.insert()
            self.link_to(parent)

    def move(self, parent):
        """
        attach self to parent
        """
        raise NotImplementedError
        assert not self.is_empty()
        assert self.site_.value == parent.site_.value
        old_path_info = self.path_info_.value
        rel_path_info = self.__get_rel_path_info()
        print(old_path_info, parent.path_info_.value)
        children = self.get_children()
        nself = self()
        nself.path_info_.value ="{}/{}".format(parent.path_info_, rel_path_info)
        print(nself.path_info_)
        self.update(nself)
        self._rev_topic_graph_.delete()
        self.link_to(parent)
        for elt in children:
            nelt = elt()
            nelt.path_info_.value = "{}/{}{}".format(
                parent.path_info_,
                rel_path_info, elt.path_info_.value.replace(
                    old_path_info, "", 1))
            print(nelt.path_info_)
            elt.update(nelt)

    def get_a_topic_function(self):
        return self._rev_a_topic_function_

    def get_not_private_posts(self):
        posts = self.db.table('collorg.communication.blog.post')
        posts.cog_oid_.value = self._rev_a_post_data_data_._post_.cog_oid_
        posts.visibility_.value = 'private', '!='
        return posts

    def get_accessible_posts(self, user):
        posts = self.get_not_private_posts()
        accessible_data = user.get_granted_data()
        other_posts = posts()
        other_posts.cog_oid_.value = \
            (self._rev_a_post_data_data_._post_ * accessible_data).cog_oid_
        posts += other_posts

        return posts

    def set_parent(self, data, link = False):
        tg = self._rev_a_post_data_post_
        tg._data_ = data
        tg.see_also_.value = link
        tg.insert()

    def winsert(self, user, **kwargs):
        data = self.db.get_elt_by_oid(kwargs['data_oid'])
        path_info = kwargs['title_']
        kwargs['text_'] = kwargs.get('text_', '')
        if data.fqtn == 'collorg.web.topic':
            if data.path_info_.value:
                if data.site_.value is not None:
                    self.site_.value = data.site_.value
                path_info = "{}/{}".format(data.path_info_, kwargs['title_'])
                if data.path_info_.value and data.path_info_.value[-1:] == '/':
                    path_info = "{}{}".format(data.path_info_, kwargs['title_'])
        self.path_info_.value = path_info
        self.cog_environment_.value = kwargs['env_oid']
        super(self.__class__, self).winsert(user, **kwargs)
        self._cog_controller.site._d_topics = None
        self._cog_controller.site.load_topics()
        return data.w3display()
