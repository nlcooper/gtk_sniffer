import adapter

def main():
    adapters = adapter.Adapter.get_adapters()
    wifi = adapters[0]
    if not len(adapters) == 1:
        print('Please choose an adapter to use:')
        for i, n in enumerate(adapters, start=1):
           print(i, n)
        choice = input('Interface number: ')
        try:
            choice = int(choice) - 1
        except:
            raise TypeError('Please input the number corresponding to your adapter.')
        wifi = adapters[choice]
    interface = adapter.Adapter(wifi)
    print(interface.name)

if __name__ == '__main__':
    print('run')
    main()
