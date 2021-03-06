#!/usr/bin/env python3

from __future__ import print_function
import os,sys
from util import PRECISION,INPUT,STATS,MEGA,GIGA

data = dict()
metadata = {}

for l in os.sys.stdin:
  m = l.split()

  if len(m) == 1 and m[0] in PRECISION.__members__:
    precision = PRECISION[m[0]]

  is_metadata = False
  if len(m) > 0 and m[0].isupper():
    metadata[l[:-1]] = 1
    is_metadata = True

  if len(m) == 2 and m[0] == "OPENMP_THREADS":
    threads = int(m[1])
  if len(m) == 2 and m[0] == "MPI_PROCS":
    procs = int(m[1])

  if not is_metadata and len(m) == INPUT.size:
    try:
      pkey = int(precision.value)
      if pkey not in data:
        data[pkey] = dict()

      wkey = int(m[INPUT.wkey])
      if wkey not in data[pkey]:
        data[pkey][wkey] = dict()

      tkey = int(m[INPUT.tkey])
      if tkey not in data[pkey][wkey]:
        data[pkey][wkey][tkey] = STATS.size*[0]
        first = True
      else:
        first = False

      entry = data[pkey][wkey][tkey]

      msec  = float(m[INPUT.msec ])
      bytes = int  (m[INPUT.bytes])
      flops = int  (m[INPUT.flops])

      if first:
        entry[STATS.msec_min] = msec
        entry[STATS.msec_med] = [msec]
        entry[STATS.msec_max] = msec
      else:
        if msec < entry[STATS.msec_min]:
          entry[STATS.msec_min] = msec
        entry[STATS.msec_med].append(msec)
        if msec > entry[STATS.msec_max]:
          entry[STATS.msec_max] = msec

      entry[STATS.bytes] = bytes
      entry[STATS.flops] = flops

    except ValueError:
      pass
for pkey in sorted(data.keys()):
  print((PRECISION(pkey).name))
  print("")
  for wkey in sorted(data[pkey].keys()):
    tdict = data[pkey][wkey]
    for tkey in sorted(tdict.keys()):
      stats = tdict[tkey]

      msec_min = stats[STATS.msec_min]

      msec_med = sorted(stats[STATS.msec_med])
      msec_med = msec_med[len(msec_med)//2]

      msec_max = stats[STATS.msec_max]

      gbytes = float(stats[STATS.bytes])/GIGA
      gflops = float(stats[STATS.flops])/GIGA

      if msec_min != 0.0 and msec_med != 0.0 and msec_max != 0.0:
        GB_sec_min = gbytes/(msec_max/MEGA)
        GB_sec_med = gbytes/(msec_med/MEGA)
        GB_sec_max = gbytes/(msec_min/MEGA)

        GFLOP_sec_min = gflops/(msec_max/MEGA)
        GFLOP_sec_med = gflops/(msec_med/MEGA)
        GFLOP_sec_max = gflops/(msec_min/MEGA)

        print(wkey,          \
              tkey,          \
              msec_min,      \
              msec_med,      \
              msec_max,      \
              GB_sec_min,    \
              GB_sec_med,    \
              GB_sec_max,    \
              GFLOP_sec_min, \
              GFLOP_sec_med, \
              GFLOP_sec_max)

    print("")

print("META_DATA")
for k,m in list(metadata.items()):
  if k != "META_DATA":
    print(k)
