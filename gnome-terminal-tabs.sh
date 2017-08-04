#!/bin/bash

xdotool_exist=$(xdotool -v > /dev/null 2>&1; echo $?)
if [[ $xdotool_exist -gt 0 ]]; then
  echo Please install xdotool.
  exit 1
fi
if [[ $(pgrep -c -u "$USER" gnome-terminal) -eq 0 ]]; then
  /usr/bin/gnome-terminal
fi
for i in $*
do
  WID=`xdotool search --class "gnome-terminal" | sort -r | head -1`
  xdotool windowfocus $WID
  xdotool key ctrl+shift+t
  xdotool type "ssh ${i}
  "
done