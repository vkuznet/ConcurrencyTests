#!/bin/bash
if [ `hostname -s` == "vocms0131" ]; then
    source /data/srv/current/sw/slc6_amd64_gcc493/external/oracle/11.2.0.4.0__10.2.0.4.0/etc/profile.d/init.sh
else
    source /data/srv/current/sw/slc7_amd64_gcc630/external/oracle/11.2.0.4.0__10.2.0.4.0/etc/profile.d/init.sh
fi
source /afs/cern.ch/user/v/valya/workspace/ConcurrencyTest/oracle-env/31/etc/profile.d/init.sh
export X509_USER_KEY=~/.globus/userkey.pem
export X509_USER_CERT=~/.globus/usercert.pem
./dbs2go -dbfile dbfile.reader -port 8800 -base ""
