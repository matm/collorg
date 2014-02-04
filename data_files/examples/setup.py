import sys
import os
from distutils.core import setup

packages = []

# borrowed from django setup.py
def fullsplit( path, result = None ):
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

for dirpath, dirnames, filenames in os.walk( "collorg_app" ):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate( dirnames ):
        if dirname.startswith( '.' ):
            del dirnames[i]
    if '__init__.py' in filenames:
        packages.append( '.'.join( fullsplit( dirpath ) ) )

if sys.version_info[:2] < (2, 7):
    print( "ERROR! collorg requires Python version 2.7 or later "
           "(%d.%d detected)." % ( sys.version_info[:2] ) )
    sys.exit(-1)

setup(name="__DB_NAME__",
      version = "0",
      url = "your url",
      license = "your license",
      platforms = ["linux"],
      packages = packages
      )
