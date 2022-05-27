import socket
import termcolor

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 2137))


login = input("login:")
password = input("Password:")

s.sendall((f"LOGIN\r\n{login}\r\n{password}\r\n\r\n").encode('utf-8'))

data = b''
while not b'\r\n\r\n' in data:
    data += s.recv(1)
    
data = data.decode('utf-8')

print(data)
params = data.split('\r\n')
status_code = int(params[0])
status_message = params[1]
data = params[2]

session = ''
if status_code == 200:
    session = data
    print("Zalogowalem sie")

    command = input("Podaj komende, wyjscie to END\n>>")
    while command != 'END':
        if command == 'MESSAGE':
            send_to = input("Wyslij do:")
            message = input("Tresc wiadomosci:")
            s.sendall((f"MESSAGE\r\n{send_to}\r\n{message}\r\nsession:{session}\r\n\r\n").encode('utf-8'))
            data = b''
            while not b'\r\n\r\n' in data:
                data += s.recv(1)
            data = data.decode('utf-8')
            params = data.split('\r\n')
            
            if params[0] != '':
                status_code = int(params[0])
                status_message = params[1]
                data = params[2]
                print(status_message, data)
            else:
                status_code = int(params[1])
                status_message = params[2]
                data = params[3]
                print(status_message, data)
            
        elif command == 'SHOW':
            s.sendall((f"SHOW\r\n{login}\r\nsession:{session}\r\n\r\n").encode('utf-8'))
            data = b''
            while not b'\r\n\r\n' in data:
                data += s.recv(1)
            data = data.decode('utf-8')
            
            params = data.split('\r\n')
            status_code = int(params[0])
            status_message = params[1]
            data = params[2]
            print(status_message, data)
            
        elif command == 'CLEAR':
            s.sendall((f"CLEAR\r\n{login}\r\nsession:{session}\r\n\r\n").encode('utf-8'))
            data = b''
            while not b'\r\n\r\n' in data:
                data += s.recv(1)
            data = data.decode('utf-8')
            
            params = data.split('\r\n')
            status_code = int(params[0])
            status_message = params[1]
            data = params[2]
            print(status_message, data)
                    
            
        elif command == 'HELP':
            print('komendy ktorych mozesz uzyc to:END, MESSAGE, HELP, SHOW, CLEAR')
        

        command = input("Podaj komende, wyjscie to END\n>>")
else:
    print(f"ERROR {status_code}/n{status_message}/n{data}")

s.sendall(('END').encode('utf-8'))
s.close()
