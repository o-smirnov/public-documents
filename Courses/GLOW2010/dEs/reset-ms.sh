#!/bin/bash

rm -fr qmc2_30s_spw0.MS
tar zxvf ../MS/qmc2_30s_spw0.MS.tgz 
wsrt_j2convert msin=qmc2_30s_spw0.MS
addbitflagcol qmc2_30s_spw0.MS
downweigh-redundant-baselines.py -I "S83 -5*" qmc2_30s_spw0.MS
python -c "import pyrap.tables; pyrap.tables.addImagingColumns('qmc2_30s_spw0.MS')"

