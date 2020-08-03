#!/usr/bin/env python

# Noah Cooper <cooper.noah@gmail.com>
            

import adapter
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from datetime import datetime
from time import sleep
class ComboBoxWindow(Gtk.Window):
    def __init__(self):
        #initialize window
        Gtk.Window.__init__(self, title="WiFi Sniffer")
        self.set_border_width(10)
        self.set_default_size(225, 250)
        self.set_resizable(False)

        #create vertifcal box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        
         #Create channel list, create label, combobox and pack them
        label = Gtk.Label()
        label.set_markup('<b>Channel</b>')
        vbox.pack_start(label, True, True, 0)
        chan = list(range(1, 14, 1)) + list(range(36, 68, 4)) + \
             list(range(100, 148, 4)) + list(range(149, 169, 4))
        channel_combo = Gtk.ComboBoxText()
        channel_combo.set_entry_text_column(0)
        channel_combo.connect('changed', self.on_channel_combo_changed)
        [channel_combo.append_text(str(x)) for x in chan]
        #for chan in channels:
        #    channel_combo.append_text(chan)
        vbox.pack_start(channel_combo, False, False, True)

        #Create width label, combobox, and pack them.
        label = Gtk.Label()
        label.set_markup('<b>Width</b>')
        vbox.pack_start(label, True, True, 0)
        widths = ['HT20', 'HT40-', 'HT40+', '80MHz']
        width_combo = Gtk.ComboBoxText()
        width_combo.set_entry_text_column(0)
        width_combo.connect('changed', self.on_width_combo_changed)
        for width in widths:
            width_combo.append_text(width)
        vbox.pack_start(width_combo, False, False, 0)

        label = Gtk.Label()
        label.set_markup('<b>Capture Status</b>')
        vbox.pack_start(label, True, True, 0)

        switch = Gtk.Switch()
        switch.connect("notify::active", self.on_switch_activated)
        switch.set_active(False)
        vbox.pack_start(switch, True, True, 0)

        self.add(vbox)

# functions to bind to signals from gui
    def on_channel_combo_changed(self, combo):
        choice = combo.get_active_text()
        interface.channel = choice
        print(interface.channel)
    def on_width_combo_changed(self, combo):
        choice = combo.get_active_text()
        interface.width = choice
        print(interface.width)
    def on_switch_activated(self, switch, gparam):
        if switch.get_active():
            interface.raise_adapter()
            sleep(1)
            interface.set_channel()
            sleep(1)
            sniff = interface.start_sniff()
        else:
            sniff.terminate()
            interface.del_adapter()
            managed.add_adapter()

            


def name_file():
    print('Using date and time for file name.')
    file_name = str(datetime.now())[:-9].replace(" ", "_").replace(
        ':', '') + "_ch{}_{}".format(channel, width)
    return file_name




def test_support():
    test = adapter.Adapter.is_supported()
    if not test:
        print('Unable to find wireless device capable of monitor mode.')
        raise SystemExit(1)

def select_adapter(adapters):
    if len(adapters) == 1:
        return adapters[0]
    print('Please choose an adapter to use:')
    for i, n in enumerate(adapters, start=1):
       print(i, n)
    choice = input('Interface number: ')
    try:
        choice = int(choice) - 1
    except:
        raise TypeError('Please input the number corresponding to your adapter.')
    return adapters[choice]


if __name__ == '__main__':
    test_support()
    ifaces = adapter.Adapter.get_adapters()
    wifi = select_adapter(ifaces)
    managed = adapter.Adapter(wifi)
    interface = adapter.Sniffer(wifi)
    managed.del_adapter()
    sleep(1)
    interface.add_adapter()
    win = ComboBoxWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()