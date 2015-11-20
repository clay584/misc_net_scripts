#!/usr/bin/env bash

# This script is used to automatically log into a number of 
# F5 devices and take ucs archives and copy them off-box.
# It will also take care of deleting old ucs archives from the 
# F5 devices as well as the local filesystem of the backup server.
#
# USE AT YOUR OWN RISK
#
# Author: Clay Curtis
# email: c l a y 5 8 4 at gmail dot com



#The local user's path the .bash_profile who's crontab will run this script
source /home/ccurtis/.bash_profile
#The local directory where the script is located...because I am no good at bash and cron.
source /home/ccurtis/projects/misc_net_scripts/f5/f5_backup/auto_backup.conf

#get datetime
F5_DATETIME="$( date +'%Y-%m-%d_%H-%M-%S' )"

#create local backup directory if it does not exist
mkdir -p "${BACKUP_DIR}"


count=0
while [ "x${DEVICES[count]}" != "x" ]
do
	CURRENT_HOST="${DEVICES[count]}"
	if [ $DEBUG -eq 1 ] ; then
		echo "connecting to ${CURRENT_HOST}..."
	fi
	ssh -i "${F5_KEY}" -l "${F5_ACCOUNT}" "${CURRENT_HOST}" /bin/bash << EOF
source ~/.bashrc
	if [ $DEBUG -eq 1 ] ; then
		echo "deleting old files on ${CURRENT_HOST} in /var/local/ucs..."
	fi
	find /var/local/ucs/*.ucs -mtime "${DAYS_TO_KEEP}" -exec rm -f {} \;
	if [ $DEBUG -eq 1 ] ; then
		echo "creating ucs archive on ${CURRENT_HOST}..."
	fi
	tmsh -c 'save sys ucs "${CURRENT_HOST}"_"${F5_DATETIME}".ucs passphrase "${UCS_PASSPHRASE}"'
EOF

	if [ $DEBUG -eq 1 ] ; then
		echo "copying ucs archive from ${CURRENT_HOST} to local filesystem ${BACKUP_DIR}..."
	fi
	scp -i "${F5_KEY}" "${F5_ACCOUNT}"@"${CURRENT_HOST}":/var/local/ucs/"${CURRENT_HOST}"_"${F5_DATETIME}".ucs "${BACKUP_DIR}"/"${CURRENT_HOST}"_"${F5_DATETIME}".ucs

	if [ $DEBUG -eq 1 ] ; then
		echo ""
		echo "-------------------------------------------"
		echo ""
	fi
	count=$[$count+1]
done

#delete old backups on local filesystem
if [ $DEBUG -eq 1 ] ; then
	echo "deleting old files on local filesystem in ${BACKUP_DIR}..."
fi
find "${BACKUP_DIR}"/* -mtime "${DAYS_TO_KEEP}" -exec rm -f {} \;
