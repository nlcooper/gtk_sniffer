#
#
# Noah Cooper
# cooper.noah@gmail.com
# Starting python3 update
#
#


import subprocess
import datetime
from time import sleep

class Incompatible(BaseException):
    """Exception for device not supporting monitor mode."""
    def __init__(self):
        super()
        print('Wireless adapter does not support monitor mode!')
        import sys
        sys.exit(0)


class interface(object):
    """Wireless Interface"""
    def __init__(self):
        self.managed_name = None
        self.monitor_name = None
        self.phy_number = None
        self.mac = None
        self.ssid = None
        self.mode = None
        self.get_name()

    @staticmethod
    def is_supported():
        """
        Checks to see if a wireless card is capable of monitor mode.
        Returns: True if supported, False if unsupported
        """
        cmd = 'iw list | grep monitor'
        stats = subprocess.check_output(cmd, shell=True).decode('utf-8')
        if 'monitor' in stats:
            return True
        else:
            return False

    def get_name(self):
        """Sets the phy# and the normal interface name"""
        cmd = ['iw', 'dev']
        info = subprocess.check_output(cmd).decode('utf-8')
        lines = info.splitlines()
        self.phy_number = 'phy{}'.format(str(lines[0])[-1])
        for line in lines:
            if 'Interface' in line:
                managed_name = line.split()[-1]
                if not managed_name == 'mon0':
                    self.managed_name = managed_name
                else:
                    self.managed_name = 'wlan0'

    def set_mon(self):
        cmd = 'sudo iw {} del'.format(self.managed_name).split()
        subprocess.call(cmd)
        sleep(0.25)
        cmd = 'sudo iw phy {} interface add mon0 type monitor'.format(self.phy_number).split()
        subprocess.call(cmd)
        sleep(0.25)
        cmd = 'sudo ip link set mon0 up'.split()
        subprocess.call(cmd)

    def set_man(self):
        cmd = 'sudo iw mon0 del'.split()
        subprocess.call(cmd)
        sleep(0.25)
        cmd = 'sudo iw phy {} interface add {} type managed'.format(self.phy_number, self.managed_name).split()
        subprocess.call(cmd)
        sleep(0.25)
        cmd = 'sudo ip link set {} up'.format(self.managed_name).split()
        subprocess.call(cmd)


def main():
    if not interface.is_supported():
        raise Incompatible
    wifi = interface()
    wifi.set_mon()
    print(wifi.ssid)
    print(wifi.mac)
    print('monitoring duder!')
    sleep(1)
    wifi.set_man()

if __name__ == '__main__':
    main()
