#! /bin/bash

NewWindow=0
kses=$(qdbus | grep konsole | head -n 1)
if [[ $kses == "" ]]; then
  NewWindow=1
  /usr/bin/konsole
  kses=$(qdbus | grep konsole | head -n 1)
fi
for i in $*
do
    if [[ $NewWindow == 0 ]]; then
      session=$(qdbus $kses /Windows/1 newSession)
    else
      session=$(qdbus $kses /Windows/1 currentSession)
    fi
    qdbus $kses /Sessions/${session} sendText "jump.sh ${i}
"
    qdbus $kses /Sessions/${session} setMonitorSilence true
done
