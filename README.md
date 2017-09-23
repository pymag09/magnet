# MAGNET
  
Magnet is a tool which helps you to SSH to host(s). It gets list of hosts from your service discovery system(for example consul), builds dictionary of keywords and associates hostname/IP with keywords.  
Magnet supports plugins. If you use custom service discovery system you can write your own plugin.  

## Why it might be useful?  
1. No need to remember hostnames/IPs  
2. If your app is installed on multiple hosts it opens all of them to save your time. You alway can use full hostname to ssh to specific host.  
3. you don't know on what host to ssh, but you probably know the app name, env, index or something. We assume that tags, lables, groups and so on are used because they are our keywords.

* `mt.py` - main interface
* `console.sh` - script which opens console of your preference (edit `console.sh` before first run)
* `mt.conf` - defines what plugin to use and path to `console.sh`
  
## Dependencies  
`python-qt4` - for GUI  
`xdotool` - for managing tabs in your terminal  

## INSTALATION
* git clone https://github.com/pymag09/magnet.git
* edit console.sh. There are number of settings at the very top of file.
    * console_tool - terminal of your preference
    * hot_key - `xdotool` emulates keys press. It's hot for new tab. Default key combinations for konosle and gnome-terminal is Ctrl+Shift+t
    * run_this - `ssh -l user `or your ssh wrapper(in case you use jump host).
    * layout_list - US layout is used when we need to type and execute some command. If you have more than one layout in the end of execution we need to revert layouts you use.
* place all (mt.conf, consul.conf, static_inventory.yaml and other config for possible plugins) config files to $HOME/.mt/ folder
* edit mt.conf. Default path is ~/.mt/. There are only two parameters.
    * plugin
    * cmd - path to console.sh script
* edit plugin config file. Default path is ~/.mt/

OPTIONAL STEP
* create hot key for mt.py. For example I use Ctrl+Alt+m.

## STATIC INVENTORY
In case you don't have everything in service discovery but want magnet to add these hosts to shared DB you can do this by adding recodrs to static_inventory.yaml, section `hosts`. Format is simple:
```
"ip or DNS name":
  - any name
  - keyword1
  - keyword2
```

## ALIASES
Another cool feature - aliases. Imagin in service discovery you have registred service - "cool.app". But in your team, everybody call this app - `fatboy`. fatboy is unofficial name and for convinience you can assigne local alias.
Format:
```
aliases:
  fatboy: cool.app
  spaceship: cool.app
  ....
```
## Terminal window
I tried different approaches, because the idea was to write single script for every possible terminal, but I end up with separate function for KDE konsole and everything else. `xdotool` has couple of downsides. All of them are related to keyboard layout. Needless to say `konsole` has perfect dbus support. Apparently this is the best choice for `konsole`. Hope this is finnaly version of `console.sh`

## DEMO  
![demo](images/magnet-demo.gif)
