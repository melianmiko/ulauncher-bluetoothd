
ulauncher-bluetoothd
=================

Bluetooth manager plugin for Ulauncher.

This plugin can connect or disconnect Bluetooth devices from
ULauncher panel. Uses `bluez` DBus API.

We're using some icons from [Papirus Icon Theme](https://github.com/PapirusDevelopmentTeam/papirus-icon-theme).

- [❓ What is ULauncher](https://ulauncher.io/)
- [💓 Donate](https://melianmiko.ru/donate)

Installation
--------------

Open Ulauncher settings, go to extensions tab and add this
extension from URL:
```
https://github.com/melianmiko/ulauncher-bluetoothd
```

Run in debug mode:
--------------------

```bash
export VERBOSE=1
export ULAUNCHER_WS_API=ws://127.0.0.1:5054/com.github.melianmiko.ulauncher-bluetoothd
export PYTHONPATH=$HOME/Projects/Ulauncher 
/usr/bin/python3 main.py
```
