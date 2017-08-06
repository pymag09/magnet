# MAGNET
  
Magnet is a tool which helps you to SSH to host(s). It gets list of hosts from your service discovery system(for example consul), builds dictionary of keywords and associates hostname/IP with keywords.  
Magnet supports plugins. If you use custom service discovery system you can write your own plugin.  

## Why it might be useful?  
1. No need to remember hostnames/IPs  
2. If your app is installed on multiple hosts it opens all of them to save your time. You alway can use full hostname to ssh to specific host.  
  
`mt.py` - main interface  
`console.sh` - script which opens console of your preference (edit `console.sh` before first run)  
`mt.conf` - defines what plugin to use and path to `console.sh`  
  
## Dependencies  
`python-qt4` - for GUI  
`xdotool` - for managing tabs in your terminal  
  
## DEMO  
![demo](images/magnet-demo.gif)
