#-*- coding: UTF-8 -*-

from collorg.orm.table import Table

class Access_aa(Table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.access.view'
    _cog_tablename = 'access_aa'
    _cog_templates_loaded = False

    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        #>>> AUTO_COG DOC. DO NOT EDIT
        """
        * _db : ref. to database. usage: self.db.table(fqtn)
        fields list:
        * function_oid_ : c_oid
        * function_name_ : string
        * goal_name_ : string
        * task_oid_ : c_oid
        * task_name_ : string
        * cog_oid_ : c_oid
        * cog_fqtn_ : c_fqtn
        * name_ : string
        * in_menu_ : bool
        * in_header_ : bool
        * in_nav_ : bool
        * icon_ : string
        * label_ : string
        * fqtn_ : text
        * cog_from_ : timestamp
        * cog_to_ : timestamp
        * data_ : c_oid
        * description_ : wiki
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Access_aa, self).__init__(db, **kwargs)

    def get_header_actions(self, l_actions, deja_vu, **kwargs):
        env = kwargs['env']
        topic = kwargs['topic']
        user = self._cog_controller.user
        av = self()
        av.in_header_.set_intention(True)
        av.function_name_.set_intention('Anonymous user', '=')
        for fqtn in env.parents_fqtns():
            av.fqtn_ +=  (fqtn, '=')
        if user is not None:
            av.function_name_ += ('Authenticated user', '=')
        av._cog_order_by = [av.name_]
        for action in av.select(fields = [
            av.cog_oid_, av.name_, av.label_, av.icon_]):
            if action.name_.value in deja_vu:
                continue
            deja_vu.append(action.name_.value)
            icon = action.w3icon(env = env, topic = topic)
            if not icon in l_actions:
                if not self._cog_controller.check_required(
                    action, **kwargs):
                        continue
                l_actions.append(icon)
        return l_actions, deja_vu

    def get_in_nav_actions(self, l_actions, **kwargs):
        env = kwargs['env']
        topic = kwargs['topic']
        user = self._cog_controller.user
        av = self()
        av.in_nav_.set_intention(True)
        av.function_name_.set_intention('Anonymous user', '=')
        for fqtn in env.parents_fqtns():
            av.fqtn_ +=  (fqtn, '=')
        if user is not None:
            av.function_name_ += ('Authenticated user', '=')
        av._cog_order_by = [av.name_]
        for action in av.select(fields = [
            av.cog_oid_, av.name_, av.label_, av.icon_]):
            link = action.w3in_nav_link(env = env, topic = topic)
            if not link in l_actions:
                if not self._cog_controller.check_required(
                    action, **kwargs):
                        continue
                l_actions.append(link)
        return l_actions
