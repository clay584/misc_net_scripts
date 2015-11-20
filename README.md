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

## F5 Auto Backup

This is a bash script to reach out via ssh and take ucs archives of F5 Big-IP devices and copy them off-box.  It also handles deleting of old ucs archives.

### Installation

1) Create an SSH keypair for this script to use for authentication if needed.
```
ssh-keygen -b 2048
```
2) Copy the keypair to each of your F5 devices you will be backing up.
```
ssh-copy-id -i ~/.ssh/id_rsa.pub backupuser@f5device.domain.com
```
3) Copy the bash script and config file to a directory on the local filesystem of your backup server.
2) Specify the path the the user's .bash_profile and the location of the script config file at the top of auto_backup.sh.
3) Modify the auto_backup.conf file to your liking, adding all of your F5 devices in the config file.
4) Add this to your local user's crontab.
```
0 0 * * *	/path/to/backup/script/auto_backup.sh >> /path/to/backup/dir/auto_backup_`date +\%Y\%m\%d\%H\%M\%S`.log 2>&1
```

### Example Output

```
[ccurtis@localhost f5_backup]$ ./auto_backup.sh 
connecting to ltm1.presidiolab.local...
deleting old files on ltm1.presidiolab.local in /var/local/ucs...
creating ucs archive on ltm1.presidiolab.local...
Saving active configuration...
/var/local/ucs/ltm1.presidiolab.local_2015-11-19_23-42-26.ucs is saved.
copying ucs archive from ltm1.presidiolab.local to local filesystem /home/ccurtis/projects/misc_net_scripts/f5/f5_backup/f5_backups...
ltm1.presidiolab.local_2015-11-19_23-42-26.ucs                                                                                                                      100% 1431KB   1.4MB/s   00:01    

-------------------------------------------

connecting to ltm3.presidiolab.local...
deleting old files on ltm3.presidiolab.local in /var/local/ucs...
creating ucs archive on ltm3.presidiolab.local...
Saving active configuration...
/var/local/ucs/ltm3.presidiolab.local_2015-11-19_23-42-26.ucs is saved.
copying ucs archive from ltm3.presidiolab.local to local filesystem /home/ccurtis/projects/misc_net_scripts/f5/f5_backup/f5_backups...
ltm3.presidiolab.local_2015-11-19_23-42-26.ucs                                                                                                                      100% 1427KB   1.4MB/s   00:01    

-------------------------------------------

connecting to gtm1.presidiolab.local...
deleting old files on gtm1.presidiolab.local in /var/local/ucs...
creating ucs archive on gtm1.presidiolab.local...
Saving active configuration...
/var/local/ucs/gtm1.presidiolab.local_2015-11-19_23-42-26.ucs is saved.
copying ucs archive from gtm1.presidiolab.local to local filesystem /home/ccurtis/projects/misc_net_scripts/f5/f5_backup/f5_backups...
gtm1.presidiolab.local_2015-11-19_23-42-26.ucs                                                                                                                      100% 1433KB 716.4KB/s   00:02    

-------------------------------------------

connecting to gtm2.presidiolab.local...
deleting old files on gtm2.presidiolab.local in /var/local/ucs...
creating ucs archive on gtm2.presidiolab.local...
Saving active configuration...
/var/local/ucs/gtm2.presidiolab.local_2015-11-19_23-42-26.ucs is saved.
copying ucs archive from gtm2.presidiolab.local to local filesystem /home/ccurtis/projects/misc_net_scripts/f5/f5_backup/f5_backups...
gtm2.presidiolab.local_2015-11-19_23-42-26.ucs                                                                                                                      100% 1434KB 716.8KB/s   00:02    

-------------------------------------------

deleting old files on local filesystem in /home/ccurtis/projects/misc_net_scripts/f5/f5_backup/f5_backups...
```
