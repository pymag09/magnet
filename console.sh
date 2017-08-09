#!/bin/bash

#
# Uncomment or add tools of your preference
# konsole default for KDE
# gnome-terminal default for unity gnome
#
console_tool="/usr/bin/konsole"
#console_tool=/usr/bin/gnome-terminal

#
# Define or change hot key for creating new tab
#
hot_key="ctrl+shift+t"

#
# Command to run
#
run_this="ssh"

hosts=$*

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
		xdotool search --onlyvisible --class $(basename $console_tool) key "$hot_key"
		xdotool search --onlyvisible --class $(basename $console_tool) type "$run_this $i
"
	done
}

#----------------
check_main_dependancies
check_if_console_is_running
xdotool search --onlyvisible --class $(basename $console_tool) windowactivate
xdotool search --onlyvisible --class $(basename $console_tool) windowfocus
setxkbmap us
xdotool search --onlyvisible --class $(basename $console_tool) windowactivate
ssh2host
