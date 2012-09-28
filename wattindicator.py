#!/usr/bin/python
# -*- coding: utf-8 -*-

from gi.repository import GObject, Gtk, AppIndicator3, GLib, UPowerGlib, Gio

class WattIndicator ():

    def __init__(self):
        # Set up DBUS
        self.bus = Gio.bus_get_sync (Gio.BusType.SYSTEM, None)

        # Find the battery path
        proxy = Gio.DBusProxy.new_sync (self.bus, Gio.DBusProxyFlags.NONE, None,
                                        "org.freedesktop.UPower", 
                                        "/org/freedesktop/UPower",
                                        "org.freedesktop.UPower", None)
        paths = proxy.EnumerateDevices ()
        self.battery_path = None
        for path in paths:
            if "battery" in path:
                self.battery_path = path
                break

        self.bus.signal_subscribe (None, 'org.freedesktop.UPower.Device', 
                                   None, None, None, 0, 
                                   lambda *args, **kwargs : self.update_watt (), None)

        self.indicator = AppIndicator3.Indicator.new ("wattindicator", "indicator-messages",
                                                      AppIndicator3.IndicatorCategory.HARDWARE)
        self.menu = Gtk.Menu ()
        self.watt_item = Gtk.MenuItem.new_with_label ("Quit")
        self.watt_item.connect ("activate", Gtk.main_quit)
        self.menu.append (self.watt_item)

        self.menu.show_all ()
        self.indicator.set_menu (self.menu)
        self.indicator.set_status (AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_attention_icon ("indicator-messages-new")
        self.indicator.set_icon("battery_plugged")

        self.client = UPowerGlib.Client.new ()

        self.update_watt ()
        
    def update_watt (self):
        if self.battery_path is None:
            self.indicator.set_label ("No battery found", "")
            return

        self.proxy = Gio.DBusProxy.new_sync(self.bus, Gio.DBusProxyFlags.NONE, None, 
                                            'org.freedesktop.UPower', 
                                            self.battery_path,
                                            'org.freedesktop.UPower.Device', 
                                            None)

        rate = self.proxy.get_cached_property ("EnergyRate").get_double ()

        if (self.client.get_on_battery ()):
            self.indicator.set_icon ("battery_plugged")
        else:
            self.indicator.set_icon ("battery-060-charging")

        self.indicator.set_label ("%.2f W" % rate, "")
        return True

if __name__ == "__main__":

    wi = WattIndicator ()
    Gtk.main ()
