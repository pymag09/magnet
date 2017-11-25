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
hosts=$*

kde_native_konsole() {
	sessionID=$(qdbus | grep konsole | head -n 1)
	for i in $hosts
	do
	    session=$(qdbus $sessionID /Windows/1 newSession)
	    qdbus $sessionID /Sessions/${session} sendText "${run_this} ${i}
	"
	    qdbus $sessionID /Sessions/${session} setMonitorSilence true
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
	sleep 1
}

ssh2host() {
	for i in $hosts; do
		xdotool key --clearmodifiers "${hot_key}"
		xdotool type --clearmodifiers "${run_this} ${i}
"
	done
}
check_main_dependancies
check_if_console_is_running
winID=$(xdotool search --onlyvisible --class $(basename $console_tool) | head -n 1)
xdotool windowactivate $winID
xdotool windowfocus $winID
if [[ $(basename $console_tool) == "konsole" ]]; then
	kde_native_konsole
else
	setxkbmap us
	ssh2host
	setxkbmap $layout_list
fi
