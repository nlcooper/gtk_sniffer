import re
import subprocess

class Adapter():
    def __init__(self, name):
        self.name = name
        self.wiphy = None
        self.mode = None
        self.MAC = None
        self.get_info()

    @staticmethod
    def get_adapters():
        cmd = 'iw dev'
        proc = subprocess.run(cmd.split(), capture_output=True, encoding='utf-8')
        return re.findall(r'Interface\s(\w*)', proc.stdout)

    @staticmethod
    def is_supported():
        cmd = 'iw list'
        proc = subprocess.run(cmd.split(), capture_output=True, encoding='utf-8')
        if not 'monitor' in proc.stdout:
            return False
        else:
            return True

    def get_info(self):
        cmd = f'iw {self.name} info'
        proc = subprocess.run(cmd.split(), capture_output=True, encoding='utf-8')
        self.wiphy = re.search(r'wiphy\s(\w)', proc.stdout)[1]
        self.MAC = re.search(r'addr\s([0-9a-f]{2}(?::[0-9a-f]{2}){5})', proc.stdout)[1]
        self.mode = re.search(r'type\s(\w*)', proc.stdout)[1]


    def del_adapter(self):
        cmd = f'iw dev {self.name} interface del'
        proc = subprocess.run(cmd.split(), capture_output=True, encoding='utf-8')
        print(proc.stdout)

    def add_adapter(self):
        cmd = f'iw phy phy{self.wiphy} interface add {self.name} type managed'
        proc = subprocess.run(cmd.split(), capture_output=True, encoding='utf-8')
        print(proc.stdout)

    def raise_adapter(self):
        cmd = f'ip link set {self.name} up'
        proc = subprocess.run(cmd.split(), capture_output=True, encoding='utf-8')
        print(proc.stdout)

    def lower_adapter(self):
        cmd = f'ip link set {self.name} down'
        proc = subprocess.run(cmd.split(), capture_output=True, encoding='utf-8')
        print(proc.stdout)


class Sniffer(Adapter):
    def __init__(self, name):
        self.channel = None
        self.width = None
        super().__init__(name)

    def add_adapter(self):
        cmd = f'iw phy phy{self.wiphy} interface add {self.name} type monitor'
        print(cmd)
        proc = subprocess.run(cmd.split(), capture_output=True, encoding='utf-8')
        print(proc.stdout)

    def start_sniff(self):
        cmd = f'tcpdump -ttttvvv -s0 -i {self.name} -w output.pcap'
        proc = subprocess.run(cmd.split(), capture_output=True, encoding='utf-8')
        print(proc.stdout)
        return proc

    def set_channel(self):
            cmd = f'iw {self.name} set channel {self.channel} {self.width}'
            proc = subprocess.run(cmd.split(), capture_output=True, encoding='utf-8')
            print(proc.stdout)

if __name__ == '__main__':
    print('run')
    a = Adapter.get_adapters()
