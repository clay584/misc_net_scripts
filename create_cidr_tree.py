#!/usr/bin/env python

# Example output:
# $ python gistfile1.py --max-prefix=23
# {'children': [{'children': [{'name': '10.100.0.0/23'},
#                             {'name': '10.100.2.0/23'}],
#                'name': '10.100.0.0/22'},
#               {'children': [{'name': '10.100.4.0/23'},
#                             {'name': '10.100.6.0/23'}],
#                'name': '10.100.4.0/22'}],
#  'name': '10.100.0.0/21'}

import argparse
from netaddr import *
import json


def get_cidr(parent, max_prefix=32):
    cidr_tree = {}
    cidr_tree['name'] = str(parent)
    if parent.prefixlen + 1 <= max_prefix:
        cidr_tree['children'] = []
        for subnet in parent.subnet(parent.prefixlen + 1):
            cidr_tree['children'].append(get_cidr(subnet, max_prefix))
    return cidr_tree


def main():
    parser = argparse.ArgumentParser(description='CIDR JSON Generator - For use with D3.js Tree Graph')

    parser.add_argument('--network', dest='parent_prefix', default='10.100.0.0/21', help='Parent CIDR block')
    parser.add_argument('--max-prefix', type=int, dest='max_length', metavar='LENGTH', default=24, help='Maximum prefix length depth')

    args = parser.parse_args()

    parent = IPNetwork(args.parent_prefix)
    tree = get_cidr(parent, args.max_length)
    print json.dumps(tree, sort_keys=True, indent=2)


if __name__ == '__main__':
    main()
