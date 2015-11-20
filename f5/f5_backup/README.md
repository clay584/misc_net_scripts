## F5 Auto Backup

This is a bash script to reach out via ssh and take ucs archives of F5 Big-IP devices and copy them off-box.  It also handles deleting of old ucs archives.  The advantage of doing it all on a remote server is that it survives F5 upgrades and the installation only has to occur on one device.

### Installation

1) Create an SSH keypair for this script to use for authentication if needed.
```
ssh-keygen -b 2048
```
2) Make sure the backup account is set for advanced shell in the F5 user configuration.

3) Copy the keypair to each of your F5 devices you will be backing up.
```
ssh-copy-id -i ~/.ssh/id_rsa.pub backupuser@f5device.domain.com
```
4) Copy the bash script and config file to a directory on the local filesystem of your backup server.

5) Specify the path the the user's .bash_profile and the location of the script config file at the top of auto_backup.sh.

6) Rename the auto_backup.conf.sample file to auto_backup.conf and change the settings to your liking, and add all of your F5 devices in the config file.

7) Add this to your local user's crontab.
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
