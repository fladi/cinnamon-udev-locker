import gi
gi.require_version('GUdev', '1.0')
gi.require_version('CScreensaver', '1.0')
from gi.repository import GUdev, GLib, CScreensaver, Gio

cs=CScreensaver.ScreenSaverProxy.new_for_bus_sync(Gio.BusType.SESSION, Gio.DBusProxyFlags.NONE, 'org.cinnamon.ScreenSaver', '/org/cinnamon/ScreenSaver', None)

def handle_event(cient, action, device):
    if not device.has_property('ID_VENDOR'):
        return
    if device.get_property('ID_VENDOR') != 'Yubico':
        return
    if action == 'remove':
        cs.call_lock('{0} removed'.format(device.get_property('ID_MODEL_FROM_DATABASE')))
    elif action == 'add':
        cs.call_simulate_user_activity()



c=GUdev.Client(subsystems=['usb'])
c.connect('uevent', handle_event)

GLib.MainLoop().run()
