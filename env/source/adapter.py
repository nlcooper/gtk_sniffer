import re
import subprocess

class Adapter():
    def __init__(self, name):
        self.name=name
        self.mode=None
        self.status=False
        self.sniff=False
        self.MAC=None

    @staticmethod
    def get_adapters():
        cmd = 'iw dev'
        proc = subprocess.run(cmd.split(), capture_output=True, encoding='utf-8')
        return re.findall('Interface\s(\w*)', proc.stdout)
        

class Sniffer(Adapter):
    def __init__(self):
        super.__init__(self)


if __name__ == '__main__':
  print('run')
  a = Adapter.get_adapters()
