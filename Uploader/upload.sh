#!/bin/bash

echo "Uploading files ...."

path=$1
env=$2
echo ${path}
echo ${env}
cd /build/upload_phts/files

case ${env} in
    "T1")
        login_usrname="phts1"
        ip="10.9.186.7"
        ;;
    "T2")
        login_usrname="phts2"
        ip="10.9.186.8"
        ;;
    "T3")
        login_usrname="phts3"
        ip="10.9.186.9"
        ;;
    *)
        echo "Invalid entry"
        ;;
esac

scp * ${login_usrname}@${ip}:/geneva/app/${login_usrname}/${path}

if [ $? -eq 0 ];then
    exit 0
else
    exit 1
fi
