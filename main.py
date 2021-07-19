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


class BluetoothExtension(Extension):
    def __init__(self):
        super(BluetoothExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        root = os.path.dirname(os.path.realpath(__file__))
        iconprop = "--icon=" + root + "/images/icon.png"

        data = event.get_data()
        action_name = "connect"
        if data[2]:
            action_name = "disconnect"

        # Get rfkill state
        res = subprocess.run(["rfkill"], stdout=subprocess.PIPE)
        res = str(res.stdout, "utf-8").split("\n")
        for a in res:
            rfdata = ' '.join(a.split())
            rfdata = rfdata.split(" ")
            if len(rfdata) > 1:
                if rfdata[1] == "bluetooth":
                    if rfdata[3] == "blocked":
                        subprocess.run(["notify-send", iconprop, 'Enabling BT controller...'])
                        subprocess.run(["rfkill", "unblock", rfdata[0]])
                        time.sleep(2)

        subprocess.run(['notify-send', iconprop, 'Trying to ' + action_name + '...', data[1]], stdout=subprocess.PIPE)
        res = subprocess.run(['bluetoothctl', action_name, data[0]], stdout=subprocess.PIPE)
        subprocess.run(["notify-send", iconprop, "BT " + action_name + " result is", str(res.stdout, "utf-8")],
                       stdout=subprocess.PIPE)


class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        result = subprocess.run(['bluetoothctl', 'paired-devices'], stdout=subprocess.PIPE)
        lines = str(result.stdout, "utf-8").split("\n")
        disconnect_key = extension.preferences.get("bt_kw2")

        for a in lines:
            columns = a.split(" ")
            if len(columns) > 2:
                name = ' '.join(columns[2:])
                items.append(ExtensionResultItem(icon='images/icon.png',
                                                 name=name,
                                                 description=columns[1],
                                                 on_enter=ExtensionCustomAction(
                                                     (columns[1], name, event.get_keyword() == disconnect_key),
                                                     keep_app_open=False)))

        return RenderResultListAction(items)


if __name__ == '__main__':
    BluetoothExtension().run()
