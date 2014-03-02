# -*- coding: utf-8 -*-

class Groupable(object):
    def __init__(self):
        self._cog_groupable = True
        self.__groups = None
        self.__events = None

    @property
    def groups(self):
        """
        retruns the groups linked to self
        """
        wg = self.db.table('collorg.group.group')
        wg.data_.value = self.cog_oid_
        return wg

    @property
    def events(self):
        """
        returns the events pointing attached to groups of the self.
        """
        return self.groups.events
