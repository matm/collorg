#!/usr/bin/env python
#-*- coding: utf-8 -*-

# ©2012 Joël Maïzi <joel.maizi@lirmm.fr>

import sys
sys.path.append('/usr/lib/python2.7/site-packages/')
import cx_Oracle
import getpass
if sys.version >= 3:
    import ordereddict
else:
    import OrederedDict as ordereddict
    input = input

ora_table = "select * from user_objects where object_name = '%s'"
ora_table_list = "select * from user_objects where object_type = 'TABLE'"
ora_view_list = "select * from user_objects where object_type = 'VIEW'"

class Dtuple(object):
    def __init__(self, dict_):
        self.dict_ = dict_
        for key, val in dict_.items():
            self.__setattr__(key, val)

    def __str__(self):
        return "%s" % (self.dict_)

class Oradb(object):
    def __init__(self, user, passwd, sid, host, port = 1521):
        self.__db = cx_Oracle.connect(user, passwd, cx_Oracle.makedsn(
            host, port, sid))

    def view(self, name):
        return Relation(self.__db, name)

    def cursor(self):
        return self.__db.cursor()

    def close(self):
        self.__db.close()

    def tables_list(self):
        extension = self.cursor().execute(ora_table_list).fetchall()
        for elt in extension:
            yield elt[0]

    def views_list(self):
        extension = self.cursor().execute(ora_view_list).fetchall()
        for elt in extension:
            yield elt[0]

class Field(object):
    def __init__(self, name, __type, idx):
        self.__ora_name = name
        self.__name = "%s_" % (name.lower())
        self.__idx = idx
        self.__is_set = False
        self.__type = __type
        self.__val = None
        self.__comp = None

    @property
    def ora_name(self):
        return self.__ora_name

    @property
    def name(self):
        return self.__name

    @property
    def type_(self):
        return self.__type

    @property
    def idx(self):
        return self.__idx

    @property
    def is_set(self):
        return self.__val is not None

    @property
    def comp(self):
        return self.__comp

    @property
    def val(self):
        return self.__val

    @property
    def quoted_val(self):
        return str(self.__val).replace("'", "''")

    def set_intention(self, val, comp = '='):
        self.__val = val
        self.__comp = comp

    def set_null(self):
        self.value = "NULL", "IS"

    def set_not_null(self):
        self.value = "NOT NULL", "IS"

    def reset(self):
        self.value = None, None

class Relation(object):
    __deja_vu = ordereddict.OrderedDict()
    def __init__(self, db, table_name):
        """relation is a raw returned by ora_table"""
        self.__cursor = db.cursor()
        self.__name = table_name
        self.__d_attrs = ordereddict.OrderedDict()
        self.__l_fields = []
        self.__req_fields = []
        self.__description = self.__get_description()
        self.__order_by = []
        self.__group_by = False

    def __get_description(self):
        if not Relation.__deja_vu.has_key(self.__name):
            self.__cursor.execute(ora_table % self.__name)
            self.__type = self.__cursor.fetchone()[4]
            self.__cursor.execute("SELECT * FROM %s WHERE 1=0" % self.__name)
            fidx = 0
            for elt in self.__cursor.description:
                field = Field(elt[0], elt[1], fidx)
                self.__setattr__(field.name, field)
                self.__d_attrs[elt[0]] = elt
                self.__l_fields.append(field)
                fidx += 1
            self.__req_fields = self.__l_fields[:]
            Relation.__deja_vu[self.__name] = self
        else:
            deja_vu = Relation.__deja_vu[self.__name]
            self.__type = deja_vu.__type
            self.__l_fields = self.__l_fields[:]
            self.__req_fields = self.__l_fields[:]
            fidx = 0
            for val in deja_vu.__d_attrs.values():
                field = Field(val[0], val[1], fidx)
                self.__setattr__(field.name, field)
                self.__d_attrs[val[0]] = val
                self.__l_fields.append(field)
                fidx += 1

    @property
    def fields(self):
        for field in self.__l_fields:
            yield(field)

    def fields_list(self):
        for field in self.__l_fields:
            yield(field.name, field.type_)

    def _sql_select(self, *args):
        if args:
            self.__req_fields = args
        else:
            self.__req_fields = self.__l_fields
        self.__extension = []
        sql = "SELECT DISTINCT %s FROM %s %s %s %s"
        what = '*'
        if args:
            _args = []
            for field in args:
                assert type(field) is Field
                _args.append(field.ora_name)
            what = ", ".join(_args)
        where = ""
        _where = []
        for field in self.__l_fields:
            if field.is_set:
                _where.append(field)
            if _where:
                where = "WHERE %s" % (" AND ".join(["%s %s '%s'" % (
                    field.ora_name, field.comp, field.quoted_val)
                    for field in _where]))
        group_by = ""
        if self.__group_by:
            what = "COUNT(*), %s" % (what)
            group_by = "GROUP BY %s" % (", ".join([
                    field.ora_name for field in self.__req_fields]))
        order_by = ""
        if self.__order_by:
            order_by = "ORDER BY %s" % (", ".join([
                    field.ora_name for field in self.__order_by]))
        sql %= (what, self.__name, where, group_by, order_by)
        return sql

    def select(self, *args):
        sql = self._sql_select(*args)
        self.__extension = self.__cursor.execute(sql).fetchall()
        return self.__extension

    def order_by(self, *args):
        self.__order_by = []
        for field in args:
            assert type(field) is Field
            self.__order_by.append(field)

    @property
    def group_by(self):
        self.__group_by = True

    def __to_dict(self, tuple_):
        dict_ = {}
        idx = 0
        got_count = False
        for field in tuple_:
            if self.__group_by and not got_count:
                dict_['__count__'] = field
                got_count = True
                continue
            dict_[self.__req_fields[idx].name] = field
            idx += 1
        return Dtuple(dict_)

    def __iter__(self):
        for tuple_ in self.__extension:
            yield self.__to_dict(tuple_)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return [self.__to_dict(self.__extension[idx])
                for idx in range(index.start, index.stop + 1)]
        else:
            return self.__to_dict(self.__extension[index])

    def __len__(self):
        return len(self.__extension)

if __name__ == '__main__':
    user = input('User: ')
    password = getpass.getpass()
    sid = input('sid: ')
    host = input('host: ')
    port = input('port [1521]: ') or '1521'
    db = Oradb(user, password, sid, host, port)
    print("Tables:\n * %s" % ("\n * ".join(db.tables_list())))
    print("Views:\n * %s" % ("\n * ".join(db.views_list())))
