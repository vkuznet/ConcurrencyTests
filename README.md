### Test setup and environment
We setup/run appropriate server (CherryPy, Flask, etc.) on cmsweb testbed
back-end nodes (vocms0131 and vocms0132):
- use run_fpy.sh script to run Flask like server
- use run_dbs2go.sh script to run dbs2go server
- run cpy_server.py to run CherryPy HTTP server
- run fpy_server.py to run Flask HTTP server

The HTTP and HTTPs servers were run on both back-end nodes. We also setup
approrpriate frontend rules (see section below) to grant access to our
back-ends via apache front-end nodes.

All tests were performed from external node (lxplus) by running appropriate
test suit using [hey](https://github.com/vkuznet/hey) tool. It was forked from
[this repository](https://github.com/rakyll/hey) and modified to support the
following features:
- parse X509 user based and proxy certificates
- add ability to read list of URLs from external file (used in random tests)

We performed the following set of tests:
- send 1000 requests with 100 concurrent clients (1k/100 notation)
- send 1000 requests with 200 concurrent clients (1k/200 notation)
- send 5000 requests with 200 concurrent clients (5k/200 notation)
- send 5000 requests with 300 concurrent clients (5k/300 notation)
We also used the following queries:
- static content, i.e. Hello World
- static DBS query, e.g. /Zee*/*/USER
- "random" DBS queries generated and stored in external file, the file
contains alternation of the following type of queries:
  - `datasets?dataset=/a/b/c`
  - `blocks?dataset=/a/b/c`
  - `files?dataset=/a/b/c`

Please see [Tests](https://github.com/vkuznet/ConcurrencyTests/Tests.md) for
full details.

### cmsweb frontend rules

##### frontend nossl rule
RewriteRule ^(/test(/.*)?)$ https://%{SERVER_NAME}${escape:$1}%{env:CMS_QUERY} [R=301,NE,L]

##### frontend ssl rule
RewriteRule ^(/test(/.*)?)$ /auth/verify${escape:$1} [QSA,PT,E=AUTH_SPEC:cert]
RewriteRule ^/auth/complete(/test(/.*)?)$ http://%{ENV:BACKEND}:8800${escape:$1} [QSA,P,L,NE]

##### authentication rule to /data/srv/current/config/frontend/backends-preprod.txt
^/auth/complete/test(?:/|$) vocms0131.cern.ch|vocms0132.cern.ch

##### restart httpd to reload applied rules
sudo service httpd reload

