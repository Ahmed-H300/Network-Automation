
import serial,time
for



with serial.Serial(port='COM6') as console:
    if console.isOpen():
        print('Serial Connection Successfully')
        console.write(b'ip route 192.168.10.5 255.255.255.0 en\n')
        time.sleep(1)

    else:
        print("Sorry you can't connect")

with serial.Serial(port='COM7') as console:
    if console.isOpen():
        print('Serial Connection Successfully')
        console.write(b'ip route 10.1.1.5 255.255.255.0 en\n')
        time.sleep(1)

    else:
        print("Sorry you can't connect")

with serial.Serial(port='COM8') as console:
    if console.isOpen():
        print('Serial Connection Successfully')
        console.write(b'ip route 192.168.11.1 255.255.255.0 en\n')
        time.sleep(1)

    else:
        print("Sorry you can't connect")

with serial.Serial(port='COM9') as console:
    if console.isOpen():
        print('Serial Connection Successfully')
        console.write(b'ip route 10.1.1.1 255.255.255.0 en\n')
        time.sleep(1)

    else:
        print("Sorry you can't connect")