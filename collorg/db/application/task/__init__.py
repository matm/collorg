#-*- coding: utf-8 -*-

from collorg.db.core.base_table import Base_table
from collorg.db.time.duration import Duration

class Task( Base_table, Duration ):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.application'
    _cog_tablename = 'task'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # REVERSE
    _rev_a_task_function_ = cog_r._rev_a_task_function_
    _rev_task_scheduler_ = cog_r._rev_task_scheduler_
    _rev_a_task_goal_ = cog_r._rev_a_task_goal_
    _rev_a_action_task_ = cog_r._rev_a_action_task_
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
        * name_ : string, PK, not null
        * delegable_ : bool
        * description_ : wiki
        """
        #<<< AUTO_COG DOC. Your code goes after
        super( Task, self ).__init__( db, **kwargs )

    @property
    def functions(self):
        return self._rev_a_task_function_._function_

    @property
    def actions(self):
        return self._rev_a_action_task_._action_

    @property
    def goals(self):
        return self._rev_a_task_goal_._goal_

    def delete(self):
        self.db.set_auto_commit(False)

        actions = self.actions
        actions_oids = [
            elt.cog_oid_.value for elt in actions.select(nodelay=True)]
        actions = actions()
        self._rev_a_action_task_.delete()
        self._rev_a_task_function_.delete()
        self._rev_a_task_goal_.delete()

        actions.cog_oid_.value = actions_oids
        actions.delete()
        super(self.__class__, self).delete()

        self.db.commit()
