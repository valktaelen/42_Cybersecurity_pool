#!/bin/bash

files="test1 test2 test3 test4"

echo "lorem ipsum" > test1
touch test2
cat /etc/fstab > test3
cat test.sh > test4

set -- $files

while true; do
    ncftp -u $MY_USER -p $MY_PASSWORD ftp_serv <<EOF
put test1
EOF
    sleep 1
    ncftp -u $MY_USER -p $MY_PASSWORD ftp_serv <<EOF
put test2
EOF
    sleep 1
    ncftp -u $MY_USER -p $MY_PASSWORD ftp_serv <<EOF
put test3
EOF
    sleep 1
    ncftp -u $MY_USER -p $MY_PASSWORD ftp_serv <<EOF
put test4
EOF
    sleep 2
    ncftp -u $MY_USER -p $MY_PASSWORD ftp_serv <<EOF
delete test1
EOF
    sleep 1
    ncftp -u $MY_USER -p $MY_PASSWORD ftp_serv <<EOF
delete test2
EOF
    sleep 1
    ncftp -u $MY_USER -p $MY_PASSWORD ftp_serv <<EOF
delete test3
EOF
    sleep 1
    ncftp -u $MY_USER -p $MY_PASSWORD ftp_serv <<EOF
delete test4
EOF
    sleep 2
done
