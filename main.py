import serial, time, xlrd
i = 1
for por in ['COM6', 'COM7', 'COM8', 'COM9']:
    with serial.Serial(port=por) as console:
        if not console.isOpen():
            print('sorry can\'t connect!')
        else:
            print(f'Serial of port {por} is connected successfully')
            # numberofbytes = console.inWaiting()
            # if numberofbytes:
            #     B = console.read(numberofbytes)
            #     data = B.decode()
            #     if 'initial configuration dialog?' in data:
            console.write(b'no\n')
            time.sleep(15)
            console.write(b'\n')
            time.sleep(1)
            console.write(b'\r\n')
            time.sleep(1)
            console.write(b'en\n')
            time.sleep(1)
            console.write(b'terminal length 0\n')
            time.sleep(1)
            console.write(b'conf t\n')
            time.sleep(1)
            book = xlrd.open_workbook('Routers_data.xlsx')
            sheet = book.sheet_by_name('Sheet1')
            data_row = sheet.row_values(i)
            host = 'hostname '+data_row[0]
            console.write(host.encode() + b'\n')
            time.sleep(1)
            console.write(b'enable secret cisco\n')
            time.sleep(1)
            console.write(b'ip domain-name local\n')
            time.sleep(1)
            console.write(b'crypto key generate rsa\n')
            time.sleep(1)
            console.write(b'2048\n')
            time.sleep(1)
            console.write(b'ip ssh version 2\n')
            time.sleep(1)
            username = data_row[1]
            password = data_row[2]
            user = 'username '+username+' password '+password
            console.write(user.encode() + b'\n')
            time.sleep(1)
            console.write(b'line vty 0 4\n')
            time.sleep(1)
            console.write(b'transport input telnet ssh\n')
            time.sleep(1)
            console.write(b'login local\n')
            time.sleep(1)
            i += 1