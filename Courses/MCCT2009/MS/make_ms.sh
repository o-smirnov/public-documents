#!/bin/bash
if [ "$1" == "" ]; then
  echo "Usage: $0 <template_name>"
  echo -n "Available templates are: "
  for t in `ls *_makems.cfg`; do
    echo -n ${t%_makems.cfg}
  done
  echo " "
  exit 1
fi

rm -f makems.cfg
ln -s $1_makems.cfg makems.cfg
makems
mv $1.MS_p1 $1.MS
