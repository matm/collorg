#-*- coding: UTF-8 -*-

from collorg.db.core.base_table import Base_table
from collorg.templates.document_type.html import Html

class Tag(Base_table):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = 'collorg.communication'
    _cog_tablename = 'tag'
    _cog_templates_loaded = False

    from .cog import relational as cog_r
    # REVERSE
    _rev_a_tag_post_ = cog_r._rev_a_tag_post_
    #<<< AUTO_COG REL_PART. Your code goes after
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
        * cog_environment_ : c_oid, inherited
        * cog_state_ : text, inherited
        * tag_ : string, PK, not null
        """
        #<<< AUTO_COG DOC. Your code goes after
        super(Tag, self).__init__(db, **kwargs)

    def search_links(self):
        vit = self.db.table('collorg.communication.view.inst_tag')
        vit.order_by(vit.data_type_, vit.tag_)
        list_ = []
        sl_ = []
        fqtn = None
        for elt in vit:
            id = Html(self).random_id()
            if fqtn and elt.data_type_.value != fqtn:
                list_.append(sl_)
                sl_ = []
            fqtn = elt.data_type_.value
            sl_.append(
                '<span id="{}" class="search_tag" '
                'title="{} post{}">{}</span>'.format(
                id, elt.count_, elt.count_.value > 1 and 's' or '', elt.tag_))
        list_.append(sl_)
        return "<hr/>".join([", ".join(sl) for sl in list_])

    def wsave(self, **kwargs):
        data = kwargs['data']
        assert data.count() == 1
        kws = [elt.strip() for elt in kwargs.get('tags', '').split(',')]
        atp = data._rev_a_tag_post_
        atp.data_type_.set_null()
        atp.delete()
        atp = data._rev_a_tag_post_
        order = atp.count()
        for kw in kws:
            if kw == '':
                continue
            order += 1
            this_kw = self()
            this_kw.tag_.value = kw
            if not this_kw.exists():
                this_kw.insert()
            atp = data._rev_a_tag_post_
            atp._tag_ = this_kw
            if not atp.exists():
                atp.order_.value = order
                atp.insert()
#        return data._rev_a_tag_post_._tag_.w3list(post=data)
