# collorg, a versatile ERP

## What is collorg?

In `collorg`, unlike many other frameworks, the development is SQL-driven. You first create your model (tables, views) in SQL and then generate the corresponding Python classes using the `cog` command. Once the Python classes have been generated, you can forget your SQL.

`Collorg` makes an intensive use of the [table inheritance implementation of PostgreSQL](http://www.postgresql.org/docs/current/static/ddl-inherit.html), allowing you to easily write applications by specializing the `communication.blog.post` table.

## Features

* A concise API:
  * Object-relational mapping (with set operators and "relational chaining"...)
  * Templating system (à la Python)
* Build a native specialized web application with:
  * a blogging system
  * users and groups access management
  * file sharing capabilities
  * LDAP authentication
  * a caching system
  * integrated debugging
* upcoming: distributed applications

## Requirements

* Any UNIX-like system supporting Python (2.7+) and Postgresql (9.2+)

## Caution

Although this framework is being used in production for more than 2 years, it is still in **alpha development** stage.
At this stage, the core model (PostgreSQL based), the API (Python) etc. are constantly evolving. 

Although there is a patching system allowing to deal with these modifications (`collorg` is agile), it is definitly not recommended for production use.
