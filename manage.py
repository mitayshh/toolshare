#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

    from django.core.management import execute_from_command_line
    
    # sanity checks
    import sys
    py_ver = "Python version: %s\n" % sys.version
    print(py_ver)

    execute_from_command_line(sys.argv)
