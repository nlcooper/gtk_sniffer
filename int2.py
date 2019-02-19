from subprocess import run
from subprocess import PIPE


def check_card():
    cmd = 'iw dev'.split()
    look = run(cmd, capture_output=True, encoding='utf-8')
    info = look.stdout.splitlines()
    phy = info[0]
    for item in info:
        if 'Interface' in item:
            name = item.split()[-1]
        if "type" in item:
            if not 'P2P' in item:
                mode = item.split()[-1]
    cmd = 'ip addr show {}'.format(name).split()
    show = run(cmd, capture_output=True, encoding='utf-8')
    found = show.stdout.splitlines()
    for item in found:
        if 'link/ether' in item:
            mac = item.split()[1]


    print(phy, name, mode, mac)







if __name__ == '__main__':
    check_card()
