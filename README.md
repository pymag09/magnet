# MAGNET
  
Magnet is a tool which helps you to SSH to host(s). It gets list of hosts from your service discovery system(for example consul), builds dictionary of keywords and associates hostname/IP with keywords.  
Magnet supports plugins. If you use custom service discovery system you can write your own plugin.

`mt.py` - main interface  
`console.sh` - script which opens console of your preference (edit `console.sh` before first run)  
`mt.conf` - defines what plugin to use and path to `console.sh`  
  
## Dependencies  
python-qt4 - for GUI  
xdotool - for managing tabs in your terminal  
  
![demo](images/magnet-demo.gif)
