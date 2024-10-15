#!/bin/bash
path="/home/data/MPEG148_TSPC_Sequence_final"
seq="NewMiniGarden"

for i in {001..300}; do
  new_num=$(printf "%03d" $((10#$i - 1)))
  oldPath="$path/$seq/Image$i.png"
  newPath="$path/$seq/Image$new_num.png"
  echo "Moving $oldPath to $newPath"
  mv "$oldPath" "$newPath"
done
