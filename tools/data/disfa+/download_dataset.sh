#!/usr/bin/env bash

DATA_DIR="../../../data/disfa+"
RAW_DIR="${DATA_DIR}/raw"
DL_URL='https://uc2a647c4cbff1a6d799b8b8bc3b.dl.dropboxusercontent.com/zip_download_get/BePpZQo1s40LAqKnzCGMSmSoQxputFXoQqzg8uGX1RsMd5HzD0uFzjoAgJuwWQje4sh8LGvoEudkYNs_mslgjg_T25SJudH3uwQnAnX8cZdBwQ?_download_id=1778106996896893287771129474689871837941957190411362697120298726&_notify_domain=www.dropbox.com&dl=1'

mkdir -p ${DATA_DIR}
mkdir -p ${RAW_DIR}

cd ${RAW_DIR}; curl "${DL_URL}" \
     -X 'GET' \
     -H 'Referer: https://www.dropbox.com/' \
     -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
     -H 'Sec-Fetch-Dest: iframe' \
     -H 'Sec-Fetch-Mode: navigate' \
     -H 'Sec-Fetch-Site: cross-site' \
     -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15' > face_dataset.zip

cd ${RAW_DIR}; unzip face_dataset.zip -d disfa+

find ${RAW_DIR} -name "*.zip"
for z in `find ${RAW_DIR} -name "*.zip"`; do
    d=`dirname $z`;
    mkdir -p $d
    unzip $z -d $d
done
