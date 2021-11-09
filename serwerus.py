import socket

    
if __name__ == '__main__':
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.bind(('localhost', 2137))
    s1.listen(5)
    
    while True:
        client1, addr = s1.accept()
        client1.send((f'CONNECTED WITH {addr[0]}').encode())
        client1.close()
        break
    
    s1.close()
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind(('localhost', 1137))
    s2.listen(5)
    
    while True:
        client2, addr = s2.accept()
        while True:
            data = client2.recv(2048)
            command = data.decode()
            
            if not command:
                break
            user_list = ['user:gustaw-password:xd']
            
            if str(command) == 'END':
                client2.send(b'closing')
                client2.close()
                break
                
            elif str(command) == 'LOGIN':
                client2.send(b'Type login:')
                user = client2.recv(2048).decode()
                client2.send(b'Type pass:')
                password = client2.recv(2048).decode()
                
                if f'user:{user}-password:{password}' in user_list:
                    client2.send(b'You have succesfully logged in!')
                else:
                    client2.send(b'wrong username or password!')