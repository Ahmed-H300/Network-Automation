import serial
import time
import xlrd

i = 1  # for routers
j = 1  # for switches


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
    # to push the initial config on all devices (routers and switches)
    for por in ['COM6', 'COM7', 'COM8', 'COM9']:
        with serial.Serial(port=por) as console:
            # check if the console is up and running
            if not console.isOpen():
                print(f'sorry can\'t connect! with {por}')
            else:
                print(f'Serial of port {por} is connected successfully')
                console.write(b'\n')
                time.sleep(1)
                console.write(b'\r\n')
                time.sleep(1)

                ######################################################
                # ### general config for both routers and switches ###
                ######################################################

                # to get console reply message size in bytes
                numberOfBytes = console.inWaiting()
                # check if it is any number more than zero
                if numberOfBytes:
                    B = console.read(numberOfBytes)
                    data = B.decode()

                    # check if that sentence exist in the console message
                    if 'initial configuration dialog?' in data:
                        console.write(b'no\n')
                        console.write(b'\n')
                        time.sleep(15)
                        console.write(b'\n')
                        time.sleep(1)
                        console.write(b'\r\n')
                        time.sleep(1)

                # to enter enable mode (to get elevated privilege[it's noted by # at the beginning])
                # in order to pass commands to the device
                console.write(b'en\n')
                time.sleep(1)
                # to show all text without having to press enter several times
                console.write(b'terminal length 0\n')
                time.sleep(1)
                # to enter configuration mode through terminal (and be able to change device config)
                console.write(b'conf t\n')
                time.sleep(1)

                #######################
                # to configure routers#
                #######################
                if por in ['COM6', 'COM7']:
                    #########################################
                    # ### general config for both routers ###
                    #########################################

                    # to open the excel file containing routers config
                    book = xlrd.open_workbook('Routers_data.xlsx')
                    sheet = book.sheet_by_name('Sheet1')

                    # get the config for the current device
                    data_row = sheet.row_values(i)
                    # compose the hostname(device name) command
                    host = 'hostname ' + data_row[0]

                    # write it to the console after encoding it
                    console.write(host.encode() + b'\n')
                    time.sleep(1)

                    # to give the device an enable mode password
                    console.write(b'enable secret cisco\n')
                    time.sleep(1)

                    # it creates a domain called local
                    console.write(b'ip domain-name local\n')
                    time.sleep(1)

                    # to generate a token
                    console.write(b'crypto key generate rsa\n')
                    time.sleep(1)
                    # of size 2024
                    console.write(b'2048\n')
                    time.sleep(5)

                    # to enable ssh
                    console.write(b'ip ssh version 2\n')
                    time.sleep(1)

                    # give it user name and password
                    username = data_row[1]
                    password = data_row[2]
                    user = 'username ' + username + ' password ' + password
                    console.write(user.encode() + b'\n')
                    time.sleep(1)

                    # allow up to 4 SSH sessions at once
                    console.write(b'line vty 0 4\n')
                    time.sleep(1)

                    # allow both telnet and SSH protocol
                    console.write(b'transport input ssh\n')
                    time.sleep(1)

                    # logins into local
                    console.write(b'login local\n')
                    time.sleep(1)

                    # ===================== router interface ================================
                    if por in ['COM6']:
                        # to get the data of only the "R1" router
                        for index in range(1, 5, 2):
                            data_row = sheet.row_values(index)

                            # to specify which interface to configure [0/X]
                            interface = 'interface ethernet 0/' + \
                                        str(int(data_row[4]))
                            console.write(interface.encode() + b'\n')
                            time.sleep(1)

                            # to give the interface an IP address [and subnet mask]
                            intf_ip = 'ip address ' + str(data_row[5]).replace('/24', ' 255.255.255.0')
                            # intf_ip = 'ip address'+" " + \    # /24 must be included in the excel sheet
                            #     str(data_row[5])+" "+"255.255.255.0"
                            console.write(intf_ip.encode() + b'\n')

                            # to keep the interface up and running
                            console.write(b'no shut \n')
                            time.sleep(1)
                            console.write(b'exit \n')
                            ip_route = 'ip route ' + str(data_row[5])[0:-4] +'0' \
                                      +' 255.255.255.0 ' +str(sheet.cell(2,5).value)[0:-3]
                            console.write(ip_route.encode() + b'\n')
                            time.sleep(3)
                        
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
                            console.write(b'no shut \n')
                            time.sleep(1)
                            console.write(b'exit \n')
                            ip_route = 'ip route ' + str(data_row[5])[0:-4] +'0' \
                                      +' 255.255.255.0 ' +str(sheet.cell(1,5).value)[0:-3]
                            console.write(ip_route.encode() + b'\n')
                            time.sleep(3)


                    console.write(b'exit \n')
                    time.sleep(1)
                    console.write(b'exit \n')
                    time.sleep(1)
                    i += 1

                # To configure switches
                else:
                    ##########################################
                    # ### general config for both switches ###
                    ##########################################

                    # to open the excel file containing switches config
                    book = xlrd.open_workbook('Switches_SSH-data.xlsx')
                    sheet = book.sheet_by_name('Sheet1')

                    # get the config for the current device
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

                    # to exit interface configuration mode
                    console.write(b'exit\n')
                    time.sleep(1)

                    username = data_row[1]
                    password = data_row[2]
                    user = 'username ' + username + ' password ' + password
                    console.write(user.encode() + b'\n')
                    time.sleep(1)

                    # open routers excel file
                    book_R = xlrd.open_workbook('Routers_data.xlsx')
                    sheet_R = book_R.sheet_by_name('Sheet1')
                    data_row_R = sheet_R.row_values(j + 2)

                    # it tell the switch about the "default-gateway"(the router IP)
                    R = data_row_R[5].split('/')
                    ip_R = 'ip default-gateway ' + R[0]
                    console.write(ip_R.encode() + b'\n')
                    time.sleep(1)

                    # creates a vlan
                    console.write(b'interface VLAN 1\n')
                    time.sleep(1)
                    S = data_row[5].split('/')
                    ip = 'ip address ' + S[0] + ' 255.255.255.0'
                    console.write(ip.encode() + b'\n')
                    console.write(b'no shut \n')
                    time.sleep(1)
                    console.write(b'exit\n')
                    time.sleep(1)
                    console.write(b'\n')
                    time.sleep(1)
                    # vlan_switch(f'switch {j} ports.xlsx')

                    ######################
                    # ### create vlans ###
                    ######################
                    vlanData = None
                    if por in ['COM8']:
                        # open excel file containing switch 1 vlans data
                        vlanData = xlrd.open_workbook('switch 1 Ports.xlsx')
                    elif por in ['COM9']:
                        # open excel file containing switch 2 vlans data
                        vlanData = xlrd.open_workbook('Switch 2 ports.xlsx')

                    sheet_vlan = vlanData.sheet_by_name('Sheet1')

                    m = 0
                    n = 0

                    for index in range(1, sheet_vlan.nrows):
                        # "oneVlan" contains the data of a single vlan
                        oneVlan = sheet_vlan.row_values(index)

                        # m/n
                        # if the "n" greater than 3
                        # let it equal 0 and increment "m" by 1
                        if n > 3:
                            n = 0
                            m += 1

                        interfaceNum = f"{m}/{n}"

                        if oneVlan[1] == 'Trunk':
                            console.write(b"interface Ethernet " + interfaceNum.encode() + b'\n')
                            time.sleep(1)
                            console.write(b"switchport trunk encapsulation dot1q\n")
                            time.sleep(1)
                            console.write(b"switchport mode trunk\n")
                            time.sleep(1)
                            trunkValue = str(oneVlan[2]).replace(':', '-')
                            console.write(b"switchport trunk allowed Vlan " + trunkValue.encode() + b'\n')
                            time.sleep(1)
                            console.write(b"exit\n")

                        elif oneVlan[1] == 'Access':
                            console.write(b"interface Ethernet " + interfaceNum.encode() + b'\n')
                            time.sleep(1)
                            console.write(b"switchport mode access\n")
                            time.sleep(1)
                            console.write(b"switchport access vlan " + str(int(oneVlan[2])).encode() + b'\n')
                            time.sleep(1)
                            console.write(b"exit\n")

                        n += 1
                    j += 1
except Exception as err:
    print('An exception was thrown!: {}'.format(err))
finally:
    print('the program will terminate now!')
