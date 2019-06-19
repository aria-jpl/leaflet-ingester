#!/bin/bash
source $HOME/verdi/bin/activate

BASE_PATH=$(dirname "${BASH_SOURCE}")

# check args
if [ "$#" -eq 2 ]; then
  thredds_data_dir=$1
  leaflet_url=$2
else
  echo "Invalid number or arguments ($#) $*" 1>&2
  exit 1
fi

# move symlinked products
INPUT_DIR=orig_symlinked_inputs
if [ ! -d "$INPUT_DIR" ]; then
   mkdir $INPUT_DIR
   mv displacement-* $INPUT_DIR/
   cd $INPUT_DIR
   cp -aL displacement-* ..
   cd ..
fi

# submit time series into leaflet server
GZ=$(find . -name "*-PARAMS.h5.gz")
unpigz ${GZ}
TS_FILE=$(find . -name "*-PARAMS.h5")
TS_PROD=$(basename $(dirname ${TS_FILE}))
mv ${TS_PROD} ${thredds_data_dir}/
TSID=${TS_PROD}/$(basename ${TS_FILE})
LURL=${leaflet_url}"?id=${TSID}"
echo "Time Series: ${TSID} ${LURL}"
${BASE_PATH}/update-leaflet-url.py ${LURL} ${TSID} || exit 1
