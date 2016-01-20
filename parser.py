#!/usr/bin/env python3
#
# author: Thiago Ribeiro
# desc: Transform OVAL xml files into python dict
#
import sys
import re
import xml.etree.ElementTree as etree
import pprint
import oval

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please, specify the xml filepath')
        sys.exit(1)

    read_file = sys.argv[1:][0]

    parse = oval.OvalParser(read_file)
    parse.get_generator()
    parse.get_definitions()
    print(parse.oval)