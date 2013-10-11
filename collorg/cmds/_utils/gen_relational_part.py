#!/usr/bin/env python
#-*- coding: utf-8 -*-

import inspect
import sys
from collorg.controller.controller import Controller
#import difflib

class GenRelationalPart():
    get_code = """def _get_%s(self):
    %s_ = self.db.table('%s')
    %s_.%s_.set_intention(self.%s_)
    return %s_\n"""

    set_code = """def _set_%s(self, %s_):
    self.%s_.set_intention(%s_.%s_)\n"""

    prop_code = """_%s_ = property(
    _get_%s, _set_%s)\n"""

    get_rev_code = """@property\ndef _rev_%s_(self):
    elt = self.db.table('%s')
    elt._%s_ = self
    if 'cog_oid_' in self.__dict__ and self.cog_oid_.value:
        if not '_cog_direct_refs' in elt.__dict__.keys():
            elt._cog_direct_refs = []
        elt._cog_direct_refs.append(self.cog_oid_.value)
    return elt\n"""

    res_cls_attr = """    _cog_schemaname = '%s'
    _cog_tablename = '%s'
    _cog_templates_loaded = False\n"""

    res_cog_ref = """    _%s_ = cog_r._%s_"""
    res_cog_rev_ref = """    _rev_%s_ = cog_r._rev_%s_"""
    res_cog_remote = """    _%s__s_ = cog_r._%s__s_ # _rev_%s_._%s_"""

    def __init__(self, controller = None):
        self.controller = controller
        if controller is None:
            self.controller = Controller()
        self.db = self.controller.db
        db_name = self.controller.db_name
        repos_path = self.controller.repos_path
        for sch in self.db.schemas:
            self.sch = sch
            for table in sch.tables:
                self.table = table
                self.fqtn = "%s.%s" % (sch.name, table)
                try:
                    self.elt = self.db.table(self.fqtn)
                except:
                    sys.stderr.write(
                        "Warning: %s not accessible!\n" % (self.fqtn))
                    continue
                rel_path = self.fqtn.replace(
                    'collorg.', 'collorg.db.').replace('.', '/')
                if self.fqtn.find('collorg.') == 0:
                    if db_name != 'collorg_db':
                        continue
                    rel_file = '%s/%s' % (repos_path, rel_path)
                else:
                    rel_file = '%s/collorg_app/%s/db/%s' % (
                        repos_path, db_name, rel_path)
                self.save_rel(self.fqtn, rel_file, sch, table)

    def __load_fields(self):
        l_fields = self.elt.db.metadata.fields_names(
            self.elt._cog_schemaname, self.elt._cog_tablename)
        res = "        self.db = db\n"
        fields = []
        for fieldname in l_fields:
            attr_fieldname = "%s_" % (fieldname)
            res += "        self.{} = Field(self, '{}')\n".format(
                attr_fieldname, fieldname)
            fields.append(attr_fieldname)
        res += "        self._cog_fields = [{}]\n".format(", ".join(
            ["self.{}".format(elt) for elt in fields]))
        return [res]

    def gen_get_code(self, f_table, field_name, fk_field_name):
        _get_code = self.get_code
        _get_code %= (
            field_name,
            field_name, f_table,
            field_name, fk_field_name, field_name,
            field_name)
        return _get_code
    
    def gen_set_code(self, field_name, fk_field_name):
        _set_code = self.set_code
        _set_code %= (
            field_name, field_name,
            field_name, field_name, fk_field_name
        )
        return _set_code
    
    def gen_prop_code(self, field_name):
        return self.prop_code % (field_name, field_name, field_name)
    
    def gen_relational(self, fqtn):
        res_cog_rel = []
        res = []
        elt = self.db.table(fqtn)
        for key, val in elt.neighbors.items():
            f_table = key
            for fkey, fval in val['l_fields'].items():
                field_name = fkey
                fk_field_name = fval
                _get_code = self.gen_get_code(
                    f_table, field_name, fk_field_name)
                _set_code = self.gen_set_code(field_name, fk_field_name)
                res_cog_rel.append("%s%s" % (_get_code, _set_code))
                res_cog_rel.append(self.gen_prop_code(field_name))
                res.append(self.res_cog_ref % (field_name, field_name))
        return res_cog_rel, res
    
    def gen_trans_rel(self, src_fqtn, fqtn):
        res = []
        try:
            elt = self.db.table(fqtn)
        except:
            print("- warning: %s not found" % (fqtn))
            return res
        for key, val in elt.neighbors.items():
            f_table = key
            if f_table == src_fqtn:
                continue
            for fkey, fval in val['l_fields'].items():
                field_name = fkey
                res.append(field_name)
        return res
    
    def gen_rev_relational(self, fqtn):
        res_cog_rel = []
        res = []
        elt = self.db.table(fqtn)
        for key, val in elt.rev_neighbors.items():
            f_table = key
            f_ref = key.rsplit(".", 1)[-1]
            append_fname = len(val) > 1
            for fkey, fval in val.items():
                lf_ref = f_ref
                if append_fname:
                    lf_ref = "%s_%s" % (f_ref, fkey)
                res_cog_rel.append(
                    self.get_rev_code % (lf_ref, f_table, fkey))
                res.append(self.res_cog_rev_ref % (lf_ref, lf_ref))
        return res_cog_rel, res
    
    def strip_lines(self, lines, begin_mark, end_mark):
        n_lines = []
        skip = False
        for line in lines:
            if skip:
                if line.rstrip() != end_mark:
                    continue
                skip = False
                continue
            if line.rstrip() == begin_mark:
                skip = True
                continue
            n_lines.append(line)
        return n_lines
    
    def replace_lines(self, lines, replact, pos):
        res = []
        idx = 1
        for line in lines:
            if idx == pos:
                for replact_line in replact:
                    res.append(replact_line)
            res.append(line.rstrip())
            idx += 1
        return res
    
    def fdl_replace(self, lines, pos):
        begin_attrs_mark = "        #>>> AUTO_COG DOC. DO NOT EDIT"
        end_attrs_mark = "        #<<< AUTO_COG DOC. Your code goes after"
        src_lines = self.strip_lines(lines, begin_attrs_mark, end_attrs_mark)
        replact = [begin_attrs_mark]
        replact += ['        """']
        replact += [
            "        * _db : ref. to database. usage: self.db.table(fqtn)"]
        replact += self.elt.showstruct()
#        replact += self.__load_fields()
        replact += ['        """']
        replact += [end_attrs_mark]
        return self.replace_lines(src_lines, replact, pos)
    
    def rel_replace(self, lines, pos):
        imp_rel = "    from .cog import relational as cog_r"
        begin_rel_mark = "    #>>> AUTO_COG REL_PART. DO NOT EDIT!"
        end_rel_mark = "    #<<< AUTO_COG REL_PART. Your code goes after"
        src_lines = self.strip_lines(lines, begin_rel_mark, end_rel_mark)
        _res_cls_attr = self.res_cls_attr % (self.sch.name, self.table)
        res_cog_rel = []
        res = []
        _res_cog_rel, _res = self.gen_relational(self.fqtn)
        got_res = len(_res_cog_rel) > 0
        if got_res:
            res += [imp_rel]
            res_cog_rel += ["# DIRECT"]
            res += ["    # DIRECT"]
            res_cog_rel += _res_cog_rel
            res += _res
        _res_rev_cog_rel, _res_rev = self.gen_rev_relational(self.fqtn)
        got_res = got_res or len(_res_rev_cog_rel)
        if len(_res_rev):
            if not res_cog_rel:
                res += [imp_rel]
            res_cog_rel += ["# REVERSE"]
            res += ["    # REVERSE"]
            res_cog_rel += _res_rev_cog_rel
            res += _res_rev
        res_rel = [begin_rel_mark]
        [res_rel.append(line) for line in _res_cls_attr.split('\n')]
        res_rel += res
        res_rel.append(end_rel_mark)
        return res_cog_rel, self.replace_lines(src_lines, res_rel, pos)

    def save_rel(self, fqtn, rel_file, sch, table, bt = False, res_cog_rel = ''):
        module_file = '%s/__init__.py' % (rel_file)
        cog_relational_file = '%s/cog/relational.py' % (rel_file)
        # the module loaded
        live_src_module = inspect.getsource(inspect.getmodule(self.elt))
        src_module = open(module_file).read()
        if src_module != live_src_module:
            sys.stderr.write("WARNING! Version mismatch!\n"
                "Skipping %s!\n"
                "Please run python setup.py install.\n\n" % (module_file))
            return
        init_src, init_start = inspect.getsourcelines(self.elt.__init__)
        init_src, cls_start = inspect.getsourcelines(self.elt.__class__)
        rel_pos = cls_start + 1
        fld_pos = init_start + 1
        lines = self.fdl_replace(open(module_file).readlines(), fld_pos)
        if not bt:
            res_cog_rel, lines = self.rel_replace(lines, rel_pos)
        open(module_file, "w").write("\n".join(lines) + "\n")
        if res_cog_rel:
            open(cog_relational_file, "w").write("\n".join(res_cog_rel) + "\n")
    
if __name__ == '__main__':
    GenRelationalPart()
