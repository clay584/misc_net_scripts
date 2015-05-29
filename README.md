# misc_net_scripts
Miscellaneous network scripts for random tasks

## create_cidr_tree.py
This script creates a nested cidr block tree in nested JSON for use with the D3.js tree collapsable tree diagram.  Input the master CIDR block and the max length you want to go in depth.

### Example

[ccurtis@shark misc_net_scripts]$ ./create_cidr_tree.py --help
usage: create_cidr_tree.py [-h] [--network PARENT_PREFIX]
                           [--max-prefix LENGTH]

CIDR JSON Generator - For use with D3.js Tree Graph

optional arguments:
  -h, --help            show this help message and exit
  --network PARENT_PREFIX
                        Parent CIDR block
  --max-prefix LENGTH   Maximum prefix length depth

[ccurtis@shark misc_net_scripts]$ ./create_cidr_tree.py --network 10.1.1.0/24 --max-prefix 29
{
  "children": [
    {
      "children": [
        {
          "children": [
            {
              "children": [
                {
                  "children": [
                    {
                      "name": "10.1.1.0/29"
                    },
                    {
                      "name": "10.1.1.8/29"
                    }
                  ],
                  "name": "10.1.1.0/28"
                },
                {
                  "children": [
                    {
                      "name": "10.1.1.16/29"
                    },
                    {
                      "name": "10.1.1.24/29"
                    }
                  ],
                  "name": "10.1.1.16/28"
...output truncated...

Output to File:

[ccurtis@shark misc_net_scripts]$ ./create_cidr_tree.py --network 10.1.1.0/24 --max-prefix 29 > cidr_tree.json


