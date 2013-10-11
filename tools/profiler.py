#!/usr/bin/env python

import pstats

pstats.Stats('/tmp/cog_profile').sort_stats('time').print_stats()
#pstats.Stats('/tmp/cog_profile').sort_stats('time').print_callers()
