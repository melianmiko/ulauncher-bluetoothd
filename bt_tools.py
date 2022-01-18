import dbus
from dbus.mainloop.glib import DBusGMainLoop

DBusGMainLoop(set_as_default=True)
system = dbus.SystemBus()

bluez = dbus.Interface(system.get_object("org.bluez", "/"),
                       "org.freedesktop.DBus.ObjectManager")


def connect(path):
    device1 = dbus.Interface(system.get_object("org.bluez", path),
                             "org.bluez.Device1")

    try:
        device1.Connect()
        return True, ""
    except dbus.exceptions.DBusException as e:
        return False, str(e)


def disconnect(path):
    device1 = dbus.Interface(system.get_object("org.bluez", path),
                             "org.bluez.Device1")

    try:
        device1.Disconnect()
        return True, ""
    except dbus.exceptions.DBusException as e:
        return False, str(e)


def get_devices():
    all_objects = bluez.GetManagedObjects()

    devices = []
    for path in all_objects:
        if "org.bluez.Device1" in all_objects[path]:
            device1 = dbus.Interface(system.get_object("org.bluez", path),
                                     "org.freedesktop.DBus.Properties")

            devices.append({
                "name": str(device1.Get("org.bluez.Device1", "Name")),
                "uuid": str(device1.Get("org.bluez.Device1", "Address")),
                "icon": str(device1.Get("org.bluez.Device1", "Icon")),
                "active": bool(device1.Get("org.bluez.Device1", "Connected")),
                "dbus_path": str(path)
            })

    return devices


if __name__ == "__main__":
    devs = get_devices()
    for a in devs:
        print(a)
