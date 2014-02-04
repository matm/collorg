= depoZ orm API

== Connection to the db

To instantiate a database object, use the {{{Db}}} class with the
{{{connect}}} method of the {{{db_connector}}} module.
The {{{connect}}} method takes only one argument: the
name of the file containing the connection parameters to the database. The file
should be in the {{{/etc/collorg/}}} directory.

{{{
from collorg.orm.db import Db
import collorg.utils.db_connector

my_database = Db( *db_connector.connect( '<db conf file name>' )
}}}

== Glossary
* schema:
* table:
* FQTN: fully qualified table name. The fully table name is unique in a
database.

== Instantiating a {{{Table}}} object
Assuming we have a table with the FQTN {{{my_schema.my_table}}}, instantiating
an object representing this table in a Python program is made using
the {{{table}}} method of the {{{Db}}} class.

{{{
my_table = my_database.table( 'my_schema.my_table' )
}}}

The object {{{my_table}}} is an instance of the
{{{collorg.orm.table.Table}}} class.

== Accessing the fields
All the field names are suffixed by an underscore: {{{field1 -> field1_}}}
to avoid potential conflicts with Python keywords (see
 [[http://www.python.org/dev/peps/pep-0008/|PEP 8]])

{{{
my_table.field1_
my_table.field2_
...
}}}

== Constraining a {{{Table}}} object
A Table represents in your Python program a table in the database. When you
instantiate a Table object you are defining the set of tuples included in
that table. There is no constraint attached to the object.
To restrict to the subset of the table you're interested in you have to
constrain the object.

=== Puting an intention on a field
The first way to constrain a Table object is to put an intention on one of
it's fields, using the {{{set_intention}}} method of the {{{Field}}} class.

{{{
my_table.field1_.set_intention( 'abc' )
}}}

On this statement you're constraining the field {{{field1}}} to the value
{{{abc}}}.
The intention of the {{{my_table}}} object refers now to the subset of elements
of {{{my_table}}} where {{{field1}}} takes the value {{{abc}}}.

