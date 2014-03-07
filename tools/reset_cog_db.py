#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os

if sys.version_info.major < 3:
    input = raw_input

description = """
WARNING!

1) THE DATABASE '%s' WILL BE REMOVED if necessary!
"""

cmd1 = """
set -x
db_name=%s
sudo apache2ctl -k restart
dropdb $db_name
createdb $db_name
%s/data_files/sql/init_db.py $db_name
"""
cmd2 = """
set -x
db_name=%s
(
cog init -d $db_name
cd $db_name
cog make
sudo python setup.py -q install
)
"""
cmd3 = """
set -x
db_name=%s
cog make
sudo python setup.py -q install
"""

if __name__ == '__main__':
    cur_dir = os.path.abspath(os.path.curdir)
    db_name = sys.argv[1]
    try:
        assert db_name.find(".") == -1
    except:
        sys.stderr.write("The database name can't contain a dot\naborting\n")
        sys.exit(1)
    print(description % (db_name))
    ok = input("proceed [N/y]? ")
    if ok.lower() != 'y':
        sys.stderr.write("aborting\n")
        sys.exit()
    print("cmd 1 %s" % (70 * "="))
    os.system(cmd1 % (db_name, cur_dir))
    if db_name != 'collorg_db':
        print("cmd 2 %s" % (70 * "="))
        os.system(cmd2 % (db_name))
    else:
        print("cmd 3 %s" % (70 * "="))
        os.system(cmd3 % (db_name))
