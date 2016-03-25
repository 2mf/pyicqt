# Copyright 2005-2006 Daniel Henninger <jadestorm@nc.rr.com>
# Licensed for distribution under the GPL version 2, check COPYING for details

import os

files = os.listdir(os.path.dirname(__file__))
for fname in files:
    if fname == "__init__.py":
        continue
    if fname.endswith(".py"):
        fname = fname.replace(".py", "")
        try:
            exec("from %s import *" % fname)
        except UnicodeDecodeError:
            print "Unable to import language %s.\n" % fname
