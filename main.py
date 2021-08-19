import serial
import time
import xlrd

i = 1
j = 1


def vlan_switch(file_name):
    pass
    # book = xlrd.open_workbook(file_name)
    # sheet = book.sheet_by_name(book.sheet_names()[0])
    # console.write(b'no \n')
    # for i in range(2, sheet.nrows):
    #                 x = sheet.row_values(i)
    #                 val = x[2]
    #                 if (type(val) == str and val.find(':')):
    #                     val= val.replace(':','-')
    #                 else:
    #                     val = str(int(val))
    #                 vlan = "vlan " + val + '\n'
    #                 console.write(vlan.encode())
    #                 console.write(b'exit \n')


try:
    for por in ['COM6', 'COM7', 'COM8', 'COM9']:
        with serial.Serial(port=por) as console:
            if not console.isOpen():
                print(f'sorry can\'t connect! with {por}')
            else:
                print(f'Serial of port {por} is connected successfully')
                console.write(b'\n')
                time.sleep(1)
                console.write(b'\r\n')
                time.sleep(1)
                numberofbytes = console.inWaiting()
                if numberofbytes:
                    B = console.read(numberofbytes)
                    data = B.decode()
                    if 'initial configuration dialog?' in data:
                        console.write(b'no\n')
                        console.write(b'\n')
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
                # to configure routers
                if por in ['COM6', 'COM7']:
                    book = xlrd.open_workbook('Routers_data.xlsx')
                    sheet = book.sheet_by_name('Sheet1')
                    data_row = sheet.row_values(i)
                    host = 'hostname ' + data_row[0]
                    console.write(host.encode() + b'\n')
                    time.sleep(1)
                    console.write(b'enable secret cisco\n')
                    time.sleep(1)
                    console.write(b'ip domain-name local\n')
                    time.sleep(1)
                    console.write(b'crypto key generate rsa\n')
                    time.sleep(1)
                    console.write(b'2048\n')
                    time.sleep(5)
                    console.write(b'ip ssh version 2\n')
                    time.sleep(1)
                    username = data_row[1]
                    password = data_row[2]
                    user = 'username ' + username + ' password ' + password
                    console.write(user.encode() + b'\n')
                    time.sleep(1)
                    console.write(b'line vty 0 4\n')
                    time.sleep(1)
                    console.write(b'transport input ssh\n')
                    time.sleep(1)
                    console.write(b'login local\n')
                    time.sleep(1)

                    # ===================== router interface ================================
                    if por in ['COM6']:
                        for index in range(1, 5, 2):
                            data_row = sheet.row_values(index)
                            interface = 'interface ethernet 0/' + \
                                        str(int(data_row[4]))
                            console.write(interface.encode() + b'\n')
                            time.sleep(1)
                            intf_ip = 'ip address ' + str(data_row[5]).replace('/24', ' 255.255.255.0')
                            # intf_ip = 'ip address'+" " + \    # /24 must be included in the excel sheet
                            #     str(data_row[5])+" "+"255.255.255.0"
                            console.write(intf_ip.encode() + b'\n')
                            time.sleep(1)
                    elif por in ['COM7']:
                        for index in range(2, 6, 2):
                            data_row = sheet.row_values(index)
                            interface = 'interface ethernet 0/' + \
                                        str(int(data_row[4]))
                            console.write(interface.encode() + b'\n')
                            time.sleep(1)
                            intf_ip = 'ip address ' + str(data_row[5]).replace('/24', ' 255.255.255.0')
                            # intf_ip = 'ip address'+" " + \
                            #     str(data_row[5])+" "+"255.255.255.0"
                            console.write(intf_ip.encode() + b'\n')
                            time.sleep(1)
                    i += 1

                # To configure switches
                else:
                    book = xlrd.open_workbook('Switches_SSH-data.xlsx')
                    sheet = book.sheet_by_name('Sheet1')
                    data_row = sheet.row_values(j)
                    host = 'hostname ' + data_row[0]
                    console.write(host.encode() + b'\n')
                    time.sleep(1)
                    console.write(b'ip domain-name local\n')
                    time.sleep(1)
                    console.write(b'crypto key generate rsa\n')
                    time.sleep(1)
                    console.write(b'2048\n')
                    time.sleep(5)
                    console.write(b'line vty 0 4\n')
                    time.sleep(1)
                    console.write(b'transport input ssh\n')
                    time.sleep(1)
                    console.write(b'login local\n')
                    time.sleep(1)
                    console.write(b'exit\n')
                    time.sleep(1)
                    username = data_row[1]
                    password = data_row[2]
                    user = 'username ' + username + ' password ' + password
                    console.write(user.encode() + b'\n')
                    time.sleep(1)
                    book_R = xlrd.open_workbook('Routers_data.xlsx')
                    sheet_R = book_R.sheet_by_name('Sheet1')
                    data_row_R = sheet_R.row_values(j+2)
                    R = data_row_R[5].split('/')
                    ip_R = 'ip default-gateway ' + R[0]
                    console.write(ip_R.encode() + b'\n')
                    time.sleep(1)
                    console.write(b'interface VLAN 1\n')
                    time.sleep(1)
                    S = data_row[5].split('/')
                    ip = 'ip address ' + S[0] + ' 255.255.255.0'
                    console.write(ip.encode() + b'\n')
                    time.sleep(1)
                    console.write(b'exit\n')
                    time.sleep(1)
                    console.write(b'\n')
                    time.sleep(1)
                    # vlan_switch(f'switch {j} ports.xlsx')
                    j += 1
except Exception as err:
    print('An exception was thrown!: {}'.format(err))
finally:
    print('the program will terminate now!')