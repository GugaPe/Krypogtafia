import socket 

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect(('localhost', 2137))
data = s1.recv(2048)
s1.close()

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect(('localhost', 1137))

while True:
    command=input('komenda:')
    s2.send(command.encode())
    response = s2.recv(2048)
    print(response.decode())
    if response.decode() == 'closing':
        break
