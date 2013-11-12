#!/usr/bin/env python

import sys
from collorg.controller.controller import Controller
import gettext

def get_page_ref(method, oid):
    return "{}-{}".format(method, oid)

ctrl = Controller()
ctrl.cog_exec_env = None
ctrl.user = None
ctrl.get_page_ref = get_page_ref
ctrl.i18n = gettext.translation('messages', '/usr/share/collorg/locale', ['fr'])
ctrl._url = sys.argv[1]
#ctrl._url_scheme, nop = ctrl._url.split('://')
db = ctrl.db
table = db.table

posts = table('collorg.communication.blog.post')
posts.visibility_.set_intention('public')
for elt in posts:
    if elt.cog_fqtn_.value != 'collorg.communication.blog.post':
        elt = elt.get()
    if elt.cog_fqtn_.value == 'collorg.web.topic':
        elt.data_type_.set_null()
        elt.action_.set_null()
    try:
        print("{} {}".format(elt.cog_fqtn_, elt.cog_oid_))
        elt._cog_get_cache('w3display')
    except:
        print("Wiping")
        elt._wipe_cache()

