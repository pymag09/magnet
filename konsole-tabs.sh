#! /bin/bash

#
# Written for KDE /usr/bin/konsole command.
# For opening new tabs in existing konsole.
#

NewWindow=0
kses=$(qdbus | grep konsole | head -n 1)
if [[ "$kses" == "" ]]; then
  NewWindow=1
  /usr/bin/konsole
  kses=$(qdbus | grep konsole | head -n 1)
fi
echo $kses >/tmp/kses
echo >>/tmp/kses
qdbus $kses >>/tmp/kses || exit
echo >>/tmp/kses
qdbus $kses /Konsole >>/tmp/kses
echo >>/tmp/kses
for i in $*
do
    echo >>/tmp/kses
    if [[ $NewWindow == 0 ]]; then
      session=$(qdbus $kses /Konsole newSession)
    else
      session=$(qdbus $kses /Konsole currentSession)
    fi
    echo $session
    echo $session >>/tmp/kses
    qdbus $kses /Sessions/${session} >>/tmp/kses
    qdbus $kses /Sessions/${session} sendText "ssh user@${i}
"
    qdbus $kses /Sessions/${session} setMonitorSilence true
done
