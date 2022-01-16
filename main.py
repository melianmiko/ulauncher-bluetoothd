import logging
import os
import subprocess
import time
import gi
gi.require_version('Gdk', '3.0')

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

logger = logging.getLogger(__name__)
notify_props = "--icon=" + os.path.dirname(os.path.realpath(__file__)) + "/images/icon.png"


def send_notification(text):
    logger.debug(text)
    subprocess.run(["notify-send", notify_props, text])


class BluetoothExtension(Extension):
    def __init__(self):
        super(BluetoothExtension, self).__init__()

        # Subscribe plugin listeners to launcher
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        search_query = event.get_argument()

        # Check current action key
        disconnect_key = extension.preferences.get("bt_kw2")
        action_name = "disconnect" if event.get_keyword() == disconnect_key else "connect"

        # Get list of paired devices from bluetoothctl output
        result = subprocess.run(['bluetoothctl', 'paired-devices'], stdout=subprocess.PIPE)
        lines = str(result.stdout, "utf-8").split("\n")

        # Parse devices list and generate items list
        items = []
        for a in lines:
            columns = a.split(" ")
            if len(columns) > 2:
                name = ' '.join(columns[2:])
                if search_query is not None and search_query not in name:
                    continue

                on_click_event = ExtensionCustomAction((columns[1], name, action_name), keep_app_open=False)
                item_row = ExtensionResultItem(icon='images/icon.png',
                                               name=name,
                                               description=columns[1],
                                               on_enter=on_click_event)

                items.append(item_row)

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        # Check, that bluetooth controller is enabled
        rfkill_data = subprocess.run(["rfkill"], stdout=subprocess.PIPE)
        rfkill_data = str(rfkill_data.stdout, "utf-8").split("\n")
        for a in rfkill_data:
            rfkill_line = ' '.join(a.split())
            rfkill_line = rfkill_line.split(" ")
            if len(rfkill_line) > 1:
                if rfkill_line[1] == "bluetooth" and rfkill_line[3] == "blocked":
                    # Re-enable bluetooth
                    logger.debug("Unlocking bluetooth device...")
                    subprocess.run(["rfkill", "unblock", rfkill_line[0]])
                    time.sleep(2)

        # Get row data
        address, name, action = event.get_data()

        # Connect and send notification
        result = subprocess.run(['bluetoothctl', action, address], stdout=subprocess.PIPE)
        result = str(result.stdout)

        if "successful" in result.lower():
            send_notification("Device " + name + " is now " + action + "ed")
        else:
            send_notification("Can't " + action + " " + name + ": " + result)


if __name__ == '__main__':
    BluetoothExtension().run()
