import sys
import os
from setuptools import setup, find_packages

collorg_version = open('data_files/version').read().strip()
python_version = sys.version_info[:2]
install_requires = [
    "psycopg2>=2.4",
    "networkx>=1.7",
    "python-creole>=1.0",
    "webob>=1.2",
    "chardet>=2.1",
    "qrcode"]

if python_version < (3, 0):
    install_requires += ["configparser>=3.2"]

scripts = ['bin/cog', 'bin/ocog']
data_files_dir = 'data_files'
def walk(the_dir, sql_files = None):
    global data_files_dir
    if sql_files is None:
        sql_files = []
    for base, dirs, files in os.walk(the_dir):
        sql_files.append(
            ('/usr/share/collorg/%s' % (base.replace(data_files_dir, '')),
             ["%s/%s" % (base, file_) for file_ in files]))
        for dir_ in dirs:
            sql_files = walk("%s/%s" % (base, dir_), sql_files)
    return sql_files
data_files = walk('data_files')

classifiers = """\
Development Status :: 1 - Planning
Intended Audience :: Developers
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Topic :: Software Development :: Libraries :: Application Frameworks
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: POSIX :: Linux
"""

if sys.version_info[:2] < (2, 7):
    print("ERROR! collorg requires Python version 2.7 or later "
        "(%d.%d detected)." % (sys.version_info[:2]))
    sys.exit(-1)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="collorg",
    version=collorg_version,
    author="Joel Maizi",
    author_email="joel@collorg.org",
    maintainer="Joel Maizi",
    maintainer_email="joel@collorg.org",
    url = "http://www.collorg.org/",
    license = "http://www.fsf.org/copyleft/gpl.html",
    platforms = ["linux"],
    install_requires = install_requires,
    description = "collorg: a versatile ERP built upon your PostgreSQL database",
    classifiers = filter(None, classifiers.split("\n")),
    long_description = "\n".join(read('README')[2:]),
    packages = find_packages(),
    scripts = scripts,
    zip_safe = True,
    data_files = data_files,
    )
