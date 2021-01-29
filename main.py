from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

import subprocess, logging, os

logger = logging.getLogger(__name__)

class DemoExtension(Extension):
    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())

class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        root = os.path.dirname(os.path.realpath(__file__))
        iconprop = "--icon="+root+"/images/icon.png"

        data = event.get_data()
        actionname = "connect"
        if data[2]: actionname = "disconnect"

        subprocess.run(['notify-send', iconprop, 'Trying to '+actionname+'...', data[1]], stdout=subprocess.PIPE)
        res = subprocess.run(['bluetoothctl', actionname, data[0]], stdout=subprocess.PIPE)
        subprocess.run(["notify-send", iconprop, "BT "+actionname+" result is", str(res.stdout, "utf-8")], stdout=subprocess.PIPE)

class KeywordQueryEventListener(EventListener):
    def on_event(self, event, extension):
        items = []
        result = subprocess.run(['bluetoothctl', 'paired-devices'], stdout=subprocess.PIPE)
        lines = str(result.stdout, "utf-8").split("\n")
        for a in lines:
            columns = a.split(" ")
            if len(columns) > 2:
                items.append(ExtensionResultItem(icon='images/icon.png',
                    name=columns[2],
                    description=columns[1],
                    on_enter=ExtensionCustomAction((columns[1], columns[2], event.get_keyword() == "btd"), 
                    keep_app_open=False)))

        return RenderResultListAction(items)

if __name__ == '__main__':
    DemoExtension().run()
