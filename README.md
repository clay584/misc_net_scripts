# Miscellaneous Network Scripts
Miscellaneous network scripts for random tasks

## Pretty IP Subnet Tree
This script creates a CIDR block tree in nested JSON for use with the D3.js tree collapsable tree diagram.  Input the master CIDR block and the max length you want to go in depth.

### Example

```
[ccurtis@shark misc_net_scripts]$ ./create_cidr_tree.py --help
usage: create_cidr_tree.py [-h] [--network PARENT_PREFIX]
                           [--max-prefix LENGTH]

CIDR JSON Generator - For use with D3.js Tree Graph

optional arguments:
  -h, --help            show this help message and exit
  --network PARENT_PREFIX
                        Parent CIDR block
  --max-prefix LENGTH   Maximum prefix length depth
```

```
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
```

Output to File:
```
[ccurtis@shark misc_net_scripts]$ ./create_cidr_tree.py --network 10.1.1.0/24 --max-prefix 29 > cidr_tree.json
```

![Alt text](/create_cidr_tree.png?raw=true "CIDR Tree in D3.js Tree Graph")

## DNS Updater

CGI-BIN app for Windows IIS to update and delete forward and reverse DNS records from web form.  It uses dnscmd.exe to perform the actual updates.

### Installation

In order to use this, you must install python on Windows, IIS, enable CGI scripts.  Then place this in CGI-BIN and run.  Also, the user account that runs IIS must be a member of DNS Admins group in AD.  Yes I know this is risky, but it was for a lab environment.

