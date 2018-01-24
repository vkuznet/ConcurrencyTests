### test hey -n 1000 -c 100

python server:
  Requests/sec: 22.4892
  [200] 920 responses

py+frontend+https:
  Requests/sec: 50.0211
  [200] 1000 responses

py+flask server:
  Requests/sec: 1121.4949
  [200] 1000 responses

python+flask+frontend:
  Requests/sec: 183.9589
  [200] 1000 responses

go-server:
  Requests/sec: 14613.8292
  [200] 1000 responses

go+frontend+https:
  Requests/sec: 159.2508
  [200] 1000 responses

go+https:
  Requests/sec: 773.1483
  [200] 1000 responses

dbs+dmwm: using https://cmsweb-testbed.cern.ch/dbs/int/global/DBSReader/datasets?dataset=/Zee*/*/*
  Requests/sec: 43.4097
  [200] 1000 responses

dbs+dmwm+random:
  Requests/sec: 48.3974
  [200] 1000 responses

dbs+flask: using https://cmsweb-testbed.cern.ch/test/?dataset=/Zee*/*/*
  Requests/sec: 157.1465
  [200] 1000 responses

dbs+flask+random:
  Requests/sec: 3.8113
  [200] 708 responses

dbs+flask+uWSGI+random:
  Requests/sec: 63.3897
  [200] 1000 responses

dbs2go+frontend: using https://cmsweb-testbed.cern.ch/test/?dataset=/Zee*/*/*
  Requests/sec: 95.6948
  [200] 1000 responses

dbs2go+frontend+random:
  Requests/sec: 157.1297
  [200] 1000 responses

dbs2go+https: using https://vocms0181.cern.ch/dbs/datasets?dataset=/Zee*/*/USER
  Requests/sec: 751.9209
  [200] 1000 responses

dbs2go+https+random:
  Requests/sec: 119.3917
  [200] 1000 responses
  using transactions
  Requests/sec: 564.9587
  [200] 1000 responses

### test hey -n 1000 -c 200

py backend:
  Requests/sec: 6.5934
  [200] 600 responses

py+frontend+https:
  Requests/sec: 42.5476
  [200] 997 responses

python flask server:
  Requests/sec: 692.4342
  [200] 1000 responses

python+flask+frontend:
  Requests/sec: 134.2846
  [200] 1000 responses

go-backend:
  Requests/sec: 11605.5850
  [200] 1000 responses

go+fronend+https:
  Requests/sec: 115.4424
  [200] 1000 responses

go+https:
  Requests/sec: 403.3322
  [200] 1000 responses

dbs+dmwm: using https://cmsweb-testbed.cern.ch/dbs/int/global/DBSReader/datasets?dataset=/Zee*/*/*
  Requests/sec: 19.2926
  [200] 953 responses
  Error distribution:
  [47]  Get https://cmsweb-testbed.cern.ch/dbs/int/global/DBSReader/datasets?dataset=/Zee*/*/*: net/http: request canceled (Client.Timeout exceeded while awaiting headers)

dbs+dmwm+random:
  Requests/sec: 44.7706
  [200] 999 responses
  Error distribution:
  [1]   Get https://cmsweb-testbed.cern.ch/dbs/int/global/DBSReader/datasets?dataset=/ZprimeToA0hToA0chichihWWTollnunu_2HDM_MZp-1400_MA0-300_13TeV-madgraph/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/AODSIM: net/http: request canceled (Client.Timeout exceeded while awaiting headers)

dbs+flask: using https://cmsweb-testbed.cern.ch/test/?dataset=/Zee*/*/*
  Requests/sec: 130.0029
  [200] 1000 responses

dbs+flask+random:
  Requests/sec: 1.0784
  [200] 108 responses

dbs+flask+uWSGI+random:
  Requests/sec: 66.9235
  [200] 1000 responses

dbs2go+frontend: using https://cmsweb-testbed.cern.ch/test/?dataset=/Zee*/*/*
  Requests/sec: 74.1807
  [200] 1000 responses

dbs2go+frontend+random:
  Requests/sec: 155.5377
  [200] 1000 responses

dbs2go+https: using https://vocms0181.cern.ch/dbs/datasets?dataset=/Zee*/*/USER
  Requests/sec: 834.3587
  [200] 1000 responses

dbs2go+https+random:
  Requests/sec: 597.6334
  [200] 1000 responses
  using transactions
  Requests/sec: 599.4425
  [200] 1000 responses

### test hey -n 5000 -c 200

py backend:
  Requests/sec: 49.1018
  [200] 4600 responses

py+frontend+https:
  Requests/sec: 67.0838
  [200] 4861 responses
  [408] 1 responses

python flask server:
  Requests/sec: 273.1616
  [200] 5000 responses

python+flask+frontend:
  Requests/sec: 346.9393
  [200] 5000 responses

go+backend:
  Requests/sec: 20211.7597
  [200] 5000 responses

go+frontend+https:
  Requests/sec: 498.6229
  [200] 5000 responses

go+https:
  Requests/sec: 1717.9714
  [200] 5000 responses

dbs+dmwm: using https://cmsweb-testbed.cern.ch/dbs/int/global/DBSReader/datasets?dataset=/Zee*/*/*
  Requests/sec: 57.2779
  [200] 4886 responses
  Error distribution:
  [67]  Get https://cmsweb-testbed.cern.ch/dbs/int/global/DBSReader/datasets?dataset=/Zee*/*/*: net/http: request canceled (Client.Timeout exceeded while awaiting headers)
  [47]  Get https://cmsweb-testbed.cern.ch/dbs/int/global/DBSReader/datasets?dataset=/Zee*/*/*: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)

dbs+dmwm+random:
  Requests/sec: 51.3909
  [200] 5000 responses

dbs+flask: using https://cmsweb-testbed.cern.ch/test/?dataset=/Zee*/*/*
  Requests/sec: 305.2126
  [200] 5000 responses

dbs+flask+random
  Requests/sec: 0.2098
  [200] 105 responses

dbs+flask+uWSGI+random:
  Requests/sec: 79.7063
  [200] 4996 responses

dbs2go+frontend: using https://cmsweb-testbed.cern.ch/test/?dataset=/Zee*/*/*
  Requests/sec: 608.0687
  [200] 5000 responses

dbs2go+frontend+random:
  Requests/sec: 549.0458
  [200] 5000 responses

dbs2go+https: using https://vocms0181.cern.ch/dbs/datasets?dataset=/Zee*/*/USER
  Requests/sec: 2339.2967
  [200] 5000 responses

dbs2go+https+random:
  Requests/sec: 738.8313
  [200] 5000 responses
  using transactions
  Requests/sec: 1630.2941
  [200] 5000 responses

### test hey -n 5000 -c 300

py-backend
  Requests/sec: 26.4857
  [200] 3820 responses

py+frontend+https:
  Requests/sec: 62.4061
  [200] 4531 responses

python flask server
  Requests/sec: 287.7402
  [200] 4800 responses

py+flask+frontend:
  Requests/sec: 265.7853
  [200] 4800 responses

go-backend:
  Requests/sec: 15802.7268
  [200] 4800 responses

go+frontend+https:
  Requests/sec: 377.9578
  [200] 4800 responses

go+https:
  Requests/sec: 1171.0620
  [200] 4800 responses

dbs+dmwm: using https://cmsweb-testbed.cern.ch/dbs/int/global/DBSReader/datasets?dataset=/Zee*/*/*
  Requests/sec: 54.2449
  [200] 4714 responses
  Error distribution:
  [49]  Get https://cmsweb-testbed.cern.ch/dbs/int/global/DBSReader/datasets?dataset=/Zee*/*/*: net/http: request canceled (Client.Timeout exceeded while awaiting headers)
  [37]  Get https://cmsweb-testbed.cern.ch/dbs/int/global/DBSReader/datasets?dataset=/Zee*/*/*: net/http: request canceled while waiting for connection (Client.Timeout exceeded while awaiting headers)

dbs+dmwm+random:
  Requests/sec: 52.1183
  [200] 4783 responses

dbs+flask: using https://cmsweb-testbed.cern.ch/test/?dataset=/Zee*/*/*
  Requests/sec: 319.7065
  [200] 4800 responses

dbs+flask+random:
  Requests/sec: 0.3244
  [200] 104 responses

dbs+flask+uWSGI+random:
  Requests/sec: 78.6781
  [200] 4777 responses

dbs2go+frontend: using https://cmsweb-testbed.cern.ch/test/?dataset=/Zee*/*/*
  Requests/sec: 335.5191
  [200] 4789 responses

dbs2go+frontend+random:
  Requests/sec: 331.0266
  [200] 4800 responses

dbs2go+https: using https://vocms0181.cern.ch/dbs/datasets?dataset=/Zee*/*/USER
  Requests/sec: 1958.2161
  [200] 4800 responses

dbs2go+https+random:
  Requests/sec: 2173.4510
  [200] 4800 responses
  using transactions
  Requests/sec: 1386.1081
  [200] 4800 responses

### test hey -n 5000 -c 500

go+https:
  Requests/sec: 776.5018
  [200] 5000 responses

### test hey -n 5000 -c 1000

go+https:
  Requests/sec: 290.3974
  [200] 5000 responses

