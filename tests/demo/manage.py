#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    demo_path = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(os.path.dirname(demo_path))
    sys.path.insert(0, base_path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.demo.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
