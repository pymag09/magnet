#!/bin/bash

##############################################################################
#
# Uncomment or add tools of your preference
# konsole default for KDE
# gnome-terminal default for unity gnome
#
console_tool="/usr/bin/konsole"
#console_tool=/usr/bin/gnome-terminal
#
#
# Define or change hot key for creating new tab
#
hot_key="Control_L+Shift_L+T"
#
# Command to run
#
run_this="ssh -l user "
#
# All your keboard layout.
#
layout_list="us,ru,ua"
#
#
##############################################################################
termID=xdotool search --onlyvisible --class $(basename $console_tool)
hosts=$*

kde_native_konsole() {
	NewWindow=0
	kses=$(qdbus | grep konsole | head -n 1)
	if [[ $kses == "" ]]; then
	  NewWindow=1
	  eval $console_tool
	  kses=$(qdbus | grep konsole | head -n 1)
	fi
	for i in $hosts
	do
	    if [[ $NewWindow == 0 ]]; then
	      session=$(qdbus $kses /Windows/1 newSession)
	    else
	      session=$(qdbus $kses /Windows/1 currentSession)
	    fi
	    qdbus $kses /Sessions/${session} sendText "${run_this} ${i}
	"
	    qdbus $kses /Sessions/${session} setMonitorSilence true
	done
}

check_main_dependancies() {
	if [[ $(xdotool -v > /dev/null 2>&1; echo $?) -gt 0 ]]; then
		echo "-----------------------"
		echo 
		echo "WARNING: Please install xdotool."
		echo
		echo "-----------------------"
		exit 1
	fi
}

check_if_console_is_running() {
	if [[ $(pgrep -c -u "$USER" "$(basename $console_tool)") -eq 0 ]]; then
 		eval $console_tool
	fi
}

ssh2host() {
	for i in $hosts; do
		xdotool key $termID "$hot_key"
		xdotool type $termID "${run_this} $i
"
	done
}

xdotool windowactivate $termID
xdotool windowfocus $termID
xdotool windowactivate $termID
if [[ $(basename $console_tool) == "konsole" ]]; then
	kde_native_konsole
else
	check_main_dependancies
    check_if_console_is_running
	setxkbmap us
	ssh2host
	setxkbmap $layout_list
fi
