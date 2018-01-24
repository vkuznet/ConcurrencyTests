#!/bin/bash

source /data/srv/current/apps/dbs/etc/profile.d/init.sh
source /afs/cern.ch/user/v/valya/workspace/ConcurrencyTest/oracle-env/31/etc/profile.d/init.sh

export X509_CAINFO=/etc/grid-security/certificates/CERN-Root-2.pem
export X509_USER_CERT=~/.globus/usercert.pem
export X509_USER_KEY=~/.globus/userkey.pem
export X509_CERT_DIR=/etc/grid-security/certificates/

export PYTHONHOME=$PYTHON_ROOT
export PYTHONPATH=/afs/cern.ch/user/v/valya/workspace/ConcurrencyTest/usr/lib/python2.7/site-packages:$PYTHONPATH
export PATH=/afs/cern.ch/user/v/valya/workspace/ConcurrencyTest/usr/bin:$PATH

# pure Flask application
#python fpy_dbs.py

# Flask running behind uWSGI
uwsgi --http-socket 0.0.0.0:8800 --wsgi-file fpy_dbs.py --callable app --processes 4 --threads 100 -b 32768
