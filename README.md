# ulauncher-bluetoothd
Ulauncher plugin to manage bluetooth devices.

This plugin allows you to connect or disconnect your Bluetooth
device directly from Ulauncher panel.

- [❓ What is ULauncher](https://ulauncher.io/)
- [💓 Donate](https://melianmiko.ru/donate)

## Installation
Open Ulauncher settings, go to extensions tab and add this
extension from URL:
```
https://github.com/melianmiko/ulauncher-bluetoothd
```

## Run in debug mode:
```bash
VERBOSE=1 ULAUNCHER_WS_API=ws://127.0.0.1:5054/com.github.melianmiko.ulauncher-bluetoothd PYTHONPATH=$HOME/Projects/Ulauncher /usr/bin/python3 main.py
```
