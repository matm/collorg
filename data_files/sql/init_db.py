#!/usr/bin/env python

import os
import sys

d_tables = {
    'core': [
        'domains.sql',
        'core/sch_core.sql',

        'core/oid_table.sql',
        #'core/abstract_table.sql',
        'core/base_table.sql',
        'core/database.sql',
        'core/namespace.sql',
        'core/data_type.sql',
        'core/view/sch.sql',
        'core/view/lost_found.sql',
        #'core/field_type.sql',
        'core/field.sql',
        'core/checked_val.sql',
        'core/patch/changelog.sql',
        ],
    'auth': [
        'auth/sch.sql',
        'auth/d_ldap.sql',
        ],
    'group': [
        'group/sch.sql',
        'group/wg_template.sql',
        'group/group.sql',
        ],
    'actor1': [
        'actor/sch.sql',
        'actor/actor.sql',
        'actor/user.sql',
        'actor/inst_group.sql',
        'actor/function.sql',
        'actor/a_function_inst_group.sql',
        'actor/relation.sql',
        ],
    'actor2': [
        'actor/category.sql',
        'actor/a_user_category.sql',
        'actor/a_function_category.sql'
        ],
    'application': [
        'application/sch.sql',
        'application/task.sql',
        'application/task_scheduler.sql',
        'application/goal.sql',
        'application/action.sql',
        'application/check.sql',
        'application/a_action_task.sql',
        'application/a_task_function.sql',
        'application/a_task_goal.sql',
        'application/view/sch.sql',
        'application/view/action_map.sql',
        'application/view/action_requirement.sql',
        ],
    'application_2': [
        'application/domain.sql',
        'application/goal.sql',
        'application/a_task_domain.sql',
        'application/a_task_goal.sql'
        ],
    'application_3': [
        'application/state.sql',
        'application/transition.sql',
        'application/log.sql'
        ],
    'time': [
        'time/sch.sql',
        'time/year.sql',
        'time/duration.sql',
        #'time/month.sql',
        #'time/day.sql',
        #'time/hour.sql',
        #'time/minute.sql'
        ],
    'planning': [
        'planning/sch.sql',
        'planning/calendar.sql',
        'planning/task.sql',
        ],
    'location':[
        'location/location.sql',
        'location/address.sql',
        'location/site.sql',
        'location/building.sql',
        'location/room.sql',
        ],
    'event': [
        'event/event.sql',
        'communication/blog/view/by_post.sql',
        'communication/blog/view/children.sql',
        #'event/a_event_calendar.sql',
        #'event/agenda_item.sql',
        #'event/agenda.sql',
        #'event/a_agenda_agenda_item.sql',
        ],
    'organization': [
        'organization/sch.sql',
        'organization/unit.sql',
        ],
    'access': [
        'access/sch_access.sql',
        'access/access.sql',
        'access/group_access.sql',
#        'access/group_access.sql',
        'access/role.sql',
        'access/hierarchy.sql',
        'access/indirect.sql',
        #'access/elt_hierarchy.sql',
        'access/view/sch.sql',
        'access/view/access_aa.sql',
        'access/view/access_ca.sql',
        'access/view/by_function.sql',
        ],
    'temporal': [
        # '_temporal/sch.sql',
        # 'temporal/year.sql',
        ],
    'directory': [
        # 'directory/sch.sql',
        # 'directory/directory.sql',
        # 'directory/address.sql',
        # 'directory/email.sql',
        # 'directory/telephone.sql',
        # 'directory/email_role.sql'
        ],
    'i18n': [
        'i18n/sch_i18n.sql',
        'i18n/language.sql',
        'i18n/translation.sql'
        ],
    'web': [
        'web/sch_web.sql',
        'web/session.sql',
        'web/site.sql',
        #'web/search.sql',
        ],
    'communication': [
        'communication/sch_communication.sql',
        'communication/comment.sql',
        'communication/follow_up.sql',
        'communication/file.sql',
        'communication/attachment.sql',
        'communication/bookmark.sql',
        'communication/blog/sch.sql',
        'communication/blog/post.sql',
        'communication/blog/a_post_data.sql',
        'communication/tag.sql',
        'communication/a_tag_post.sql',
        'communication/view/sch.sql',
        'communication/view/inst_tag.sql',
        'communication/blog/view/sch.sql',
        ],
    'web2': [
        'web/topic.sql',
        'web/wall.sql',
    ],
    'documentation': [
        'documentation/sch_documentation.sql',
        'documentation/document.sql',
        'documentation/part.sql',
        'documentation/paragraph.sql',
        'documentation/comment.sql'
        ],
    'after': [
        'actor/user_s_photo.sql',
        'group/definition.sql',
        'access/a_topic_function.sql',
        'access/view/access.sql',
        'group/view/sch.sql',
        'group/view/membership.sql',
        'access/view/topic_access.sql',
        'application/communication/sch.sql',
        'application/communication/ticket.sql',
        'application/communication/error.sql',
        'application/communication/error_traceback.sql',
        'web/rss.sql',
        'web/a_rss_topic.sql',
        'communication/user_check.sql',
        'communication/poll.sql',
        'communication/view/comment.sql',
    ]
}

schemas = [
    'core', 'time', 'auth', 'group', 'actor1', 'actor2', 'application',
    'organization', 'web', 'access', 'planning', 'application_3' ]
schemas += [ 'i18n', 'communication', 'web2', 'location', 'event' ]
schemas += [ 'after' ]

if __name__ == '__main__':
    db_name = sys.argv[1]
    path = '/'.join( sys.argv[0].split( '/' )[:-1] )
    res = os.system(
        "psql %s -c 'SELECT idx(array[11], 22)' > /dev/null 2>& 1" % (
            db_name ) )
    if res != 0:
        sys.stderr.write( "postgresql intarray extension is missing\n" )
        sys.exit( 1 )
    for schema in schemas:
        for table in d_tables[schema]:
            os.system( "psql %s -f %s/%s 2>& 1 | grep -v NOTICE" % (
                db_name, path, table ) )
