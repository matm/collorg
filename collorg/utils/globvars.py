import sys
import os
if sys.version_info[0] < 3:
    import ConfigParser as configparser
else:
    import configparser

def cog_pkg_path(db_name):
    if db_name != 'collorg_db':
        return "collorg_app/%s/db" % db_name
    return "collorg/db"

templates_dir = "cog/templates"

cog_config_template = """[core]
    database = %s
"""

setup_template = """import sys
import os
from distutils.core import setup

schemas = []

# borrowed from django setup.py
def fullsplit(path, result = None):
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

for dirpath, dirnames, filenames in os.walk("collorg_app"):
    # Ignore dirnames that start with '.' 
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'):
            del dirnames[i]
    if '__init__.py' in filenames:
        schemas.append('.'.join(fullsplit(dirpath)))

if sys.version_info[:2] < (2, 7):
    print("ERROR! collorg requires Python version 2.7 or later "
           "(%%d.%%d detected)." %% (sys.version_info[:2]))
    sys.exit(-1)

setup(name="%s",
      version = "0",
      url = "your url",
      license = "your license",
      platforms = ["linux"],
      packages = schemas)

"""

cog_config = """[core]
database = %s
"""

module_template = """#-*- coding: %s -*-

%s

class %s(%s):
    #>>> AUTO_COG REL_PART. DO NOT EDIT!
    _cog_schemaname = '%s'
    _cog_tablename = '%s'
    _cog_templates_loaded = False
    #<<< AUTO_COG REL_PART. Your code goes after
    def __init__(self, db, **kwargs):
        super(%s, self).__init__(db, **kwargs)

"""

def _get_cog_config_file(path, ref_dir):
    if os.path.exists('.cog/config'):
        return '%s/.cog/config' % (os.path.abspath(os.path.curdir))
    if os.path.abspath(os.path.curdir) != '/':
        return _get_cog_config_file(os.chdir('..'), ref_dir)
    os.chdir(ref_dir)
    return None

def _config(section, elt):
    ref_dir = os.path.abspath(os.path.curdir)
    val = None
    config_parser = configparser.ConfigParser()
    conf_file = _get_cog_config_file(os.path.curdir, ref_dir)
    if conf_file:
        config_parser.read(conf_file)
        val = config_parser.get(section, elt)
    return val
