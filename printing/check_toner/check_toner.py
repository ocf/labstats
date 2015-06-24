#!/usr/bin/env python3
import sys
from ocflib.printing.printers import get_toner

if __name__ == '__main__':
    print("/".join(map(str, get_toner(sys.argv[1]))))
