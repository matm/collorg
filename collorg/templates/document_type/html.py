#!/usr/bin/env python
#-*- coding: utf-8 -*-

### Copyright © 2011 Joël Maïzi <joel.maizi@lirmm.fr>
### This file is part of collorg

### collorg is free software: you can redistribute it and/or modify
### it under the terms of the GNU General Public License as published by
### the Free Software Foundation, either version 3 of the License, or
### (at your option) any later version.

### This program is distributed in the hope that it will be useful,
### but WITHOUT ANY WARRANTY; without even the implied warranty of
### MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
### GNU General Public License for more details.

### You should have received a copy of the GNU General Public License
### along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
shorthand to some of the most common HTML5 elements
They can be used in the templates, example:
* html(self).a().hidden().label("blah").css("class", "blue")
* html(self).li()
* html(self).table(self.field_1, self.field_3)
* html(self).form(?)
* html(self).upload()
* html(self)...
"""

import sys
if sys.version >= '3':
    unicode = str

from creole import creole2html
import urllib
import cgi
from random import random

from collorg.db.communication.comment import Comment

class Html():
    def __init__(self, elt):
        self.__elt = elt
        self.__html = '%s'
        self.__charset = self.__elt._cog_controller._charset
        self._ = self.__elt._cog_controller.i18n.gettext

    def __call__(self, elt = None):
        if elt:
            self.__elt = elt
        return Html(self.__elt)

    def set_html_id(self, obj, method_name):
        return "%s_%s_%s" % (
            obj.__class__.__name__, method_name, Html(obj).random_id())

    def add_json_res(self, dict_):
        """
        dict_ constains {key:val} where key an elt of the dom.
        (css notation)
        """
        self.__elt._cog_controller.add_json_res(dict_)

    def __href(self, **kwargs):
        res = []
        kwargs['cog_fqtn_'] = self.__elt.fqtn
        if 'cog_ref_oid' in kwargs.keys():
            if not 'cog_fqtn_' in kwargs and not 'cog_oid_' in kwargs:
                kwargs['cog_fqtn_'] = self.__elt.fqtn
        for key, val in kwargs.items():
            if val is None:
                continue
            res.append('%s=%s' % (
                urllib.quote(key), urllib.quote("%s" % val)))
        if res:
            return '?{}'.format("&amp;".join(res))
        return ""

    def pre(self, html):
        self.__html = '<pre>%s</pre>' % (cgi.escape("%s" % (html)))
        return self

    def __get_oid_or_pk(self, elt, **kwargs):
        """
        adds to kwargs cog_oid_ or the pk fields
        """
        if 'cog_proxy_oid' in kwargs.keys():
            # we must have elt.cog_oid_
            kwargs['cog_oid_'] = kwargs['cog_proxy_oid']
            kwargs['cog_elt_oid'] = "{}".format(elt.cog_oid_)
        elif 'cog_oid_' in elt.__dict__:
            kwargs['cog_oid_'] = "{}".format(elt.cog_oid_)
        else:
            #!! elt is a pview (?? pkey for a pview ??)
            for field in elt._cog_pkey_fields:
                kwargs["%s_" % (field.name)] = "{}".format(field)
        if 'cog_oid_' in kwargs.keys() and kwargs["cog_oid_"] == "None":
            kwargs["cog_oid_"] = None
        return kwargs

    def a(
        self,
        cog_method='w3display', cog_fqtn=False, target='#cog_container',
        label=None, title='', css_class=None, id_="", page_ref="",
        a_attrs=(), href=None, just_href=False, **kwargs):
        """
        iterates if cog_fqtn is False.
        """
        kw = {}
        for key, val in kwargs.items():
            kw[key] = val
        if not 'cog_raw' in kwargs:
            css_class = (
                css_class and
                ' class="action %s"' % (css_class) or
                ' class="action"')
        else:
            css_class = 'class="{}"'.format(css_class)
        id_ = id_ and ' id="{}"'.format(id_)
        kw['cog_method'] = cog_method
        oid = None
        if 'cog_oid_' in self.__elt.__dict__ and self.__elt.cog_oid_:
            oid = "{}".format(self.__elt.cog_oid_)
        page_ref = 'page_ref="{}"'.format(
            self.__elt._cog_controller.get_page_ref(cog_method, oid))
        kw.pop('method', None)
        html = []
        the_target = target
        the_label = label
        try:
            self.__elt.order_by(*self.__elt.cog_label_fields)
        except:
            #XXX FIX NEEDED HERE
            # If the label returns self._other_.get()._cog_label,
            # we end up here.
            pass
        if not cog_fqtn:
            #!! cog_oid_ is integrated in pview
            elt = self.__elt
            kw = self.__get_oid_or_pk(elt, **kw)
            label = the_label
            if not label:
                label = elt.cog_label()
            target = the_target and ' target="%s"' % (the_target) or ''
        else:
            kw['cog_fqtn_'] = self.__elt.fqtn
        if just_href:
            return self.__href(**kw)
        std_href = self.absolute_link(just_href=True)
        if the_target == '_blank':
            std_href = self.__href(**kw)
        target = the_target and ' target="%s"' % (the_target) or ''
        title = title and ' title="{}"'.format(title)
        html.append("""<a %s %s %s %s %s %s %s %s>%s</a>""" % (
            'href="{}"'.format(std_href),
            'data-href="{}"'.format(href or self.__href(**kw)),
            " ".join([elt for elt in a_attrs]),
            target, css_class, id_, page_ref, title, label))
        if html:
            try:
                self.__html = self.__html % tuple(html)
            except TypeError as err:
                self.__html = ("<pre>Error: %s\nself.__html:\n"
                    "%s\nhtml:%s\nkwargs: %s\nlen(html):%s</pre>" % (
                        err, self.__html, html, kw, len(html)))
        return self

    def absolute_link(self, just_href = False):
        href = "{}/{}".format(
            self.__elt._cog_controller._url,
            self.__elt.cog_oid_)
        if just_href:
            return href
        href = '<a href="{}">{}</a>'.format(href, self.__elt.cog_label())
        return href

    def ul(self, css_class = ''):
        css_class = css_class and ' class="%s"' % (css_class)
        self.__html = self.__html % ('<ul%s>%%s</ul>' % (css_class))
        return self

    def li(self):
        html = self.__elt.count() * '<li>%s</li>'
        self.__html = self.__html % html
        return self

    def select(
        self, name, value_field, label_field=None, default=None,
        message = None,
        live=False,
        trigger_elt=None,
        trigger_method="w3display",
        trigger_target="#cog_container",
        width=None,
        **kwargs):
        """
        name: the name of the varialbe returned
        label_field: optional (_cog_label) if not provided
        trigger_elt: a hidden html().a() elt that will be triggered
        """
        if message is None:
            message = self._('select an entry')
        live_html = ''
        live_class = ''
        if live:
            live_class = ' class="live"'
        style = ''
        trigger_select = ''
        if trigger_elt:
            trigger_select = '''trigger="True"'''
        if width:
            style='style="width:%s;"' % (width)
        html = '<select name="%s" %s %s %s>' % (
            name, live_class, style, trigger_select)
        if self.__elt.count() > 1:
            dis_selected = 'disabled="disabled"'
            if not default:
                dis_selected = 'selected="selected"'
            html += '''<option value="" %s>%s</option>''' % (
                dis_selected, message)
        selected_ok = False
        for elt in self.__elt.get_extent():
            value=elt.__dict__[value_field.pyname].val
            trigger = ''
            id_ = self.random_id()
            if live:
                kwargs[name] = value
                live_elt = Html(elt)
                if trigger_elt:
                    live_elt = Html(trigger_elt)
                live_html += live_elt.a(
                    cog_method=trigger_method,
                    target=trigger_target,
                    a_attrs = ('id="%s"' % (id_),),
                    **kwargs).__html
                trigger = 'class="action" triggered="#%s"' % (id_)
            selected = ''
            if default is not None and not selected_ok:
                if elt.cog_oid_.val == default.cog_oid_.val:
                    selected = 'selected="selected"'
                    selected_ok = True
            if label_field:
                label = elt.__dict__[label_field.pyname].val
            else:
                label = elt.cog_label()
            html += '<option value="%s" %s %s>%s</option>' % (
                value, selected, trigger, label)
        if live_html:
            live_html = '<div class="hidden">%s</div>' % (live_html)
        html += '</select>'
        self.__html = self.__html % ("%s%s" % (html, live_html))
        return self

    def radio_checkbox(
        self,
        type_,
        name, value_field, label_field, checked_values, **kwargs):
        """
        radio or checkbox
        """
        html = []
        input_radio = ('<label>%s '
            '<div class="right"><input type="%s" name="%s" value="%s" %s>'
            '</div></label>')
        for elt in self.__elt:
            label = ""
            if label_field:
                label = elt.__dict__[label_field.pyname].value
            value = elt.__dict__[value_field.pyname].value
            checked = ''
            if checked_values is not None and value in checked_values:
                checked = 'checked="checked"'
            html.append(input_radio % (
                label, type_, name, value, checked))
        self.__html = self.__html % '%s' % ("<br/>".join(html))
        return self

    def radio(
        self,
        name, value_field, label_field, checked_values = None, **kwargs):
        return self.radio_checkbox(
            'radio',
            name, value_field, label_field, checked_values, **kwargs)

    def checkbox(
        self,
        name, value_field, label_field, checked_values = None, **kwargs):
        return self.radio_checkbox(
            'checkbox',
            name, value_field, label_field, checked_values, **kwargs)

    def input(self,
               field,
               id_ = None,
               name = None,
               label = None,
               directive = '',
               hidden = False,
               rows = 20,
               inline = False,
               css_class = '',
               **kwargs):
        """
        * acts according to the sql type of the field (wiki, string... see
          postgresql domains)
        * if the field.name is cog_oid and field.val is None replace
          name by cog_fqtn and value by field.table.fqtn
        Dependencies:
        * works with the plugin jquery.validate.js
        """
        comments = ""
#        if not hidden and field.table.cog_oid_.val:
#            comments = Comment(field.table.db).w3list_link(
#                data=field.table, field=field, follow_up="ok")
        wikicreole_link = (
            '<a href="http://www.wikicreole.org/attach/CheatSheet/creole_cheat_sheet.png" ' +
            'target="blank_"><em>wiki creole</em></a>')
        textarea = ['wiki', 'text']
        match_type = ['email', 'password']
        html_label = '<label for="%s"><b>%s</b></label> '
        html_input = '%s%s<input id="%s" %s %s type="%s" name="%s" value="%s" />%s'
        html_textarea =(
            '%s %%s%%s<div class="%s"><textarea id="%%s" %%s %%s %%s ' +
            'rows="%s" name="%%s">%%s</textarea>%%s</div>' +
            '<div class="render_wiki"></div>')

        css_class = css_class and ' class="%s"' % (css_class)
        name = name or '%s_' % (field.name)
        required = field.is_required and ' required="required"' or ''
        rid = id_ or self.random_id(name)
        label = label or field.name.replace('_', ' ').capitalize().strip()
        label = self._(label)
        value = kwargs.get('value', None)
        if value is None:
            value = field.value
            if value is None:
                value = ''
        if name == 'cog_oid_' and not value:
            name = 'cog_fqtn_'
            value = field.table.fqtn
        hidden = (hidden and 'hidden="hidden"') or ''
        if hidden:
            label = ''
        type_ = 'text'
        if field.sql_type in match_type:
            type_ = field.sql_type
        if hidden:
            type_ = 'hidden'
        view_wiki = ''
        edit_wiki = ''
        if field.sql_type == 'wiki' and not hidden:
            view_wiki = '<span class="button vwiki" target="#{}">{}</span>'\
                .format(rid, self._("preview"))
            edit_wiki = ('<span class="button ewiki hidden" '
                'target="#{}">{}</span>').format(rid, self._("edit"))
        if field.sql_type in textarea:
            html_input = html_textarea % (
                field.sql_type == 'wiki' and " (%s)" % wikicreole_link or '',
                field.sql_type, rows)
            type_ = ''
        if required and not hidden:
            label = '{} <span class="required"><em>{}</em></span>'.\
                format(label, self._("required"))
        self.__html = "%s%s %s" % (label and html_label % (rid, label),
                    directive,
                    html_input % (
                        view_wiki, edit_wiki,
                        rid, required, css_class, type_,
                        name, value, comments))
        if not inline:
            self.__html = '<div class="highlight"><p>%s</p></div>' % (
                self.__html)
        return self

    def form(
        self,
        html,
        method = 'POST',
        tag='form',
        css_class = '',
        name = '',
        id = '',
        reset = False,
        **kwargs):
        """
        should insert the reference of the calling object (self.__elt)
        as hidden input
        """
        assert tag == 'form' or tag == 'div' or tag == 'span'
        # nested forms don't work with safari!!
        attrs = ''
        attrs += css_class and ' class="%s"' % (css_class) or ''
        attrs += name and ' name="%s"' % (name) or ''
        attrs += id and ' id="%s"' % (id) or ''
        assert method.upper() == 'POST' or method.upper() == 'GET'
        if tag == 'form':
            method = 'method="%s"' % (method)
        else:
            method = '' #html5 compliance
        if kwargs:
            attrs += " ".join(
                ['%s="%s"' % (key, val) for key, val in kwargs.items()])
        self.__html = '<%s %s %s>%s</%s>' % (
            tag, attrs, method, html, tag)
        return self

    def random_id(self, name = ''):
        return "id_%s_%s_%s" % (
            name, int(random() * 100000), int(random() * 100000))

    def __repr__(self):
        return self.__html


    def display(self,
               field,
               label = None,
               css_class = '',
               comments_enabled = False,
               highlight = True,
               follow_up = 'ok',
               **kwargs):
        """
        display a field
        """
        comments = ""
        if comments_enabled:
            comments = Comment(field.table.db).w3list_link(
                data=field.table, field=field, follow_up=follow_up)
        if highlight:
            css_class = "higlight %s" % css_class
        css_class = css_class and ' class="%s"' % (css_class)
        if label is None:
            label = field.name.replace('_', ' ').capitalize()
        value = field.val
        if value is None or value == '':
            return ''
        if field.sql_type in ('wiki', 'text'):
            if label: # '' and no label
                label = '<h5>%s</h5>' % label
            if field.sql_type == 'wiki':
                value = self.creole(value)
            else:
                value = value.replace('>', '&gt;').replace('<', '&lt;')
            return '<div %s>%s%s%s</div>' % (
                css_class, label, value, comments)
        if label != "":
            label = "<b>%s</b>:" % (label)
        value = value.replace('>', '&gt;').replace('<', '&lt;')
        return '<div %s>%s %s %s</div>' % (
            css_class, label, value, comments)

    def creole(self, val):
        if val is None:
            return ""
        if not type(val) is unicode:
            val = unicode(val, self.__charset)
        return creole2html(val).encode(self.__charset)
