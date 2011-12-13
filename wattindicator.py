#!/usr/bin/python
# -*- coding: utf-8 -*-

from gi.repository import GObject, Gtk, AppIndicator3, GLib, UPowerGlib
import subprocess, re

class WattIndicator ():
    def __init__(self):
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
        self.indicator.set_icon("battery_full")

        self.client = UPowerGlib.Client.new ()

        self.update_watt ()
        self.timer = GLib.timeout_add (15000, self.update_watt)
        
    def update_watt (self):
        p = subprocess.Popen (["upower", "-d"], stdout=subprocess.PIPE)
        output = p.communicate()[0]

        if (self.client.get_on_battery ()):
            self.indicator.set_icon ("battery_full")
        else:
            self.indicator.set_icon ("battery-060-charging")

        matches = re.findall (r"energy-rate:[\s|\t]+(\d+\.\d+)", output)
        if (len(matches) == 0):
            print("No matches")
            return True
        else:
            self.indicator.set_label ("%s W" % matches[0], "")
            return True

if __name__ == "__main__":

    wi = WattIndicator ()
    Gtk.main ()
