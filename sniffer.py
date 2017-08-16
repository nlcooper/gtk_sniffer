#!/usr/bin/env python
'''
Noah Cooper <cooper.noah@gmail.com>
            <noahcooper@allionusa.com>

requires gksu to be installed

'sudo apt update && sudo apt install gksu'

once gksu is installed, launch anywhere with

'gksudo python /path/to/sniffer.py'

pcap files are generated in directory in which the program is run
'''

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import subprocess
from subprocess import Popen, check_output, call
import sys
from datetime import datetime

#initialize global variables

channel = ''
width = ''
interface = ''
dump = ''
capfile = ''


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
        chan = range(1, 14, 1) + range(36, 68, 4) + range(100, 148, 4) + range(
            149, 169, 4)
        channels = list()
        for i in chan:
            channels.append(str(i))
        channel_combo = Gtk.ComboBoxText()
        channel_combo.set_entry_text_column(0)
        channel_combo.connect('changed', self.on_channel_combo_changed)
        for chan in channels:
            channel_combo.append_text(chan)
        vbox.pack_start(channel_combo, False, False, True)

        #Create width label, combobox, and pack them.
        label = Gtk.Label()
        label.set_markup('<b>Width</b>')
        vbox.pack_start(label, True, True, 0)
        widths = ['HT20', 'HT40-', 'HT40+']
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
        global channel
        channel = choice

    def on_width_combo_changed(self, combo):
        choice = combo.get_active_text()
        global width
        width = choice

    def on_switch_activated(self, switch, gparam):
        '''
        capture using tcpdump using settings when toggled, return to managed
        mode when toggling back to off
        '''
        if switch.get_active():
            print('Disconnecting from any wireless network...')
            disconnect()
            print('Putting {} into monitor mode...'.format(interface))
            delete()
            enable_monitor()
            print('Bringing {} back up...'.format(interface))
            up()
            call(
                'iw {} set channel {} {}'.format(interface, channel, width),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True)
            global capfile
            capfile = name_file()
            print(
                'Writing output from {} on channel {} with a width of {} to {}'.
                format(interface, channel, width, capfile))
            global dump
            dump = Popen(
                'tcpdump -i {} -ttvvv -s 0 -w {}.pcap'.format(
                    interface, capfile),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True)
        else:
            print('Closing {}...'.format(capfile))
            dump.terminate()
            print('Switching to managed mode...')
            delete()
            disable_monitor()
            print('Bringing {} up'.format(interface))
            up()
            print('Attempting to reconnect to wireless network...')


def name_file():
    '''
    name capture file using date and time
    '''
    print('Using date and time for file name.')
    file_name = str(datetime.now())[:-9].replace(" ", "_").replace(
        ':', '') + "_ch{}_{}".format(channel, width)
    return file_name


def delete():
    '''
    delete interface
    '''
    try:
        call(
            'iw dev {} del'.format(interface),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
    except:
        sys.exit('Unable to delete wireless interface')


def connect():
    '''
    connect to network using NetworkManager command line
    '''
    try:
        call(
            'nmcli d connect {}'.format(interface),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
    except:
        print(
            'Failed to connect to network using nmcli. You will have to manually reconnect.'
        )


def disconnect():
    '''
    disconnect from network using NetworkManager command line
    '''
    try:
        call(
            'nmcli d disconnect {}'.format(interface),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
    except:
        print('Failed to disconnect from wireless network!')


def down():
    try:
        check_output(
            'ip link set {} down'.format(interface),
            stdout=subprocess.PIPE,
            stderr=suprocess.PIPE,
            shell=True)
    except:
        print('Failed to bring down {}'.format(interface))


def up():
    try:
        call(
            'ip link set {} up'.format(interface),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
    except:
        print('Failed to bring up {}'.format(interface))


def enable_monitor():
    try:
        call(
            'iw phy phy0 interface add {} type monitor'.format(interface),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)

    except:
        print('Failed to create monitor interface with {}.'.format(interface))


def disable_monitor():
    try:
        call(
            'iw phy phy0 interface add {} type managed'.format(interface),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
    except:
        print('Failed to disable monitor mode on {}'.format(interface))


def find_adapter():
    try:
        adapter_output = subprocess.check_output(['iw', 'dev']).split()
        x = adapter_output.index('Interface')
        adapter = adapter_output[x + 1]
        print(
            'Found a wireless adapter named {0}, using it for capture device.'.
            format(adapter))
        return adapter
    except:
        sys.exit('Failed to find wireless interface!')


if __name__ == '__main__':
    interface = find_adapter()
    win = ComboBoxWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
