import adapter

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

def main():
    test_support()
    tryit = adapter.Adapter.is_supported()
    ifaces = adapter.Adapter.get_adapters()
    wifi = select_adapter(ifaces)
    interface = adapter.Adapter(wifi)
    print(interface.name)
    print(interface.wiphy)
    print(interface.MAC)
    print(interface.mode)
    print(interface.channel)
    print(interface.width)
    print(interface.center)
if __name__ == '__main__':
    print('run')
    main()
