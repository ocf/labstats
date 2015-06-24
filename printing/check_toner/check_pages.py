#!/usr/bin/env python3
import sys
from ocflib.printing.printers import get_lifetime_pages

if __name__ == '__main__':
    print(get_lifetime_pages(sys.argv[1]))
