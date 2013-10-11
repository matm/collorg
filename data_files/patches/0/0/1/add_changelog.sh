#!/bin/bash

set -e
psql $1 -f /usr/share/collorg/sql/core/patch/changelog.sql
cog make
