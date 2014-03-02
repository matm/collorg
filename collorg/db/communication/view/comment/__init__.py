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
        post = self.db.table('collorg.communication.blog.post')
        post.cog_oid_.value = self.post_oid_.value
        post.title_.value = self.post_title_.value
        return post

    def comment(self):
        comment = self.db.table('collorg.communication.comment')
        comment.cog_oid_.value = self.comment_oid_.value
        comment.cog_creat_date_.value = self.comment_creat_date_.value
        comment.cog_modif_date_.value = self.comment_modif_date_.value
        comment.text_.value = self.comment_text_.value
        return comment

    def comment_author(self):
        author = self.db.table('collorg.actor.user')
        author.cog_oid_.value = self.user_comment_oid_.value
        author.first_name_.value = self.user_comment_first_name_.value
        author.last_name_.value = self.user_comment_last_name_.value
        return author

    def follow_up(self):
        fu = self.db.table('collorg.communication.follow_up')
        fu.cog_oid_.value = self.follow_up_oid_.value
        fu.cog_creat_date_.value = self.follow_up_creat_date_.value
        fu.cog_modif_date_.value = self.follow_up_modif_date_.value
        fu.text_.value = self.follow_up_text_.value
        return fu

    def follow_up_author(self):
        fua = self.db.table('collorg.actor.user')
        fua.cog_oid_.value = self.user_follow_up_oid_.value
        fua.first_name_.value = self.user_follow_up_first_name_.value
        fua.last_name_.value = self.user_follow_up_last_name_.value
        return fua

    desc = {'post':{('comment', 'comment_author'):('follow_up', 'follow_up_author')}}
