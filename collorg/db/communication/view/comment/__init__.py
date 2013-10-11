#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Comment(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication.view'
    _cog_tablename = 'comment'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    user = None
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * post_oid_ : c_oid
        * post_title_ : string
        * post_author_ : c_oid
        * comment_oid_ : c_oid
        * comment_creat_date_ : timestamp
        * comment_modif_date_ : timestamp
        * comment_text_ : wiki
        * user_comment_oid_ : c_oid
        * user_comment_first_name_ : string
        * user_comment_last_name_ : string
        * follow_up_oid_ : c_oid
        * follow_up_creat_date_ : timestamp
        * follow_up_modif_date_ : timestamp
        * follow_up_text_ : wiki
        * user_follow_up_oid_ : c_oid
        * user_follow_up_first_name_ : string
        * user_follow_up_last_name_ : string
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Comment, self).__init__(db, **kwargs)

    def post(self):
        return self.set_class_variable(
            'collorg.communication.blog.post',
            ('cog_oid_', 'post_oid_'),
            ('title_', 'post_title_'))

    def comment(self):
        return self.set_class_variable(
            'collorg.communication.comment',
            ('cog_oid_', 'comment_oid_'),
            ('cog_creat_date_', 'comment_creat_date_'),
            ('cog_modif_date_', 'comment_modif_date_'),
            ('text_', 'comment_text_'))

    def comment_author(self):
        return self.set_class_variable(
            'collorg.actor.user',
            ('cog_oid_', 'user_comment_oid_'),
            ('first_name_', 'user_comment_first_name_'),
            ('last_name_', 'user_comment_last_name_'))

    def follow_up(self):
        return self.set_class_variable(
            'collorg.communication.follow_up',
            ('cog_oid_', 'follow_up_oid_'),
            ('cog_creat_date_', 'follow_up_creat_date_'),
            ('cog_modif_date_', 'follow_up_modif_date_'),
            ('text_', 'follow_up_text_'))

    def follow_up_author(self):
        return self.set_class_variable(
            'collorg.actor.user',
            ('cog_oid_', 'user_follow_up_oid_'),
            ('first_name_', 'user_follow_up_first_name_'),
            ('last_name_', 'user_follow_up_last_name_'))

    desc = {'post':{('comment', 'comment_author'):('follow_up', 'follow_up_author')}}
