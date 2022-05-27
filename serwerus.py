import socket
from _thread import *
import os
import uuid
import termcolor

ip_connection = ('localhost', 2137)

def send_response(socket_connection, status_code, data):
    code_description = ''

    if status_code == 200:
        os.system('color 20')
        code_description = termcolor.colored("Sucess!", "green")
    elif status_code == 210:
        os.system('color 20')
        code_description = termcolor.colored("No messages", "green")
    elif status_code == 300:
        os.system('color 40')
        code_description = termcolor.colored("Wrong command", "red")
    elif status_code == 404:
        os.system('color 40')
        code_description = termcolor.colored("Wrong params for command", "red")
    elif status_code == 500:
        os.system('color 40')
        code_description = termcolor.colored("You are not authorised user.", "red")
    else:
        os.system('color 0')
        code_description = termcolor.colored("Something went wrong! Unexpected error.", "yellow")
        
    socket_connection.sendall((str(status_code) + '\r\n' + code_description +'\r\n' + data + '\r\n\r\n').encode('utf-8'))


users = {'guga': 'xd', 'gugu': 'xdd'}

auth_users = []

messages = []

def server_client(client):
    global userMessage
    data = ''
    while 'END' not in data:
        data = b''
        while not b'\r\n\r\n' in data:
            data += client.recv(1)
        data = data.decode('utf-8')
        print(data,'\r\n')
        if 'LOGIN' in data:
            params = data.split("\r\n")
            
            if params[1] in users and users[params[1]] == params[2]:
                session_id = uuid.uuid4().hex
                auth_users.append(session_id)
                send_response(client, 200, session_id)
            else:
                send_response(client, 404, "User or pass is wrong!")
            
        elif 'MESSAGE' in data:
            if 'session' in data:
                session = data.split('session:')[1].split('\r\n')[0]
                print(session)
            else:
                session = False
            params = data.split("\r\n")
            
            if session_id == False or session not in auth_users:
                send_response(client, 500, "Please log in.")
            
            elif params[1] == params[2] == '' or params[1] not in users:
                    send_response(client, 404, "User doesnt exist")
            
            else:
                messages.append( ( params[1], params[2]) )
                send_response(client, 200, "Sent!")
                print(messages)
                
                
        elif 'SHOW' in data:
            if 'session' in data:
                session = data.split('session:')[1].split('\r\n')[0]
                print(session)
            else:
                session = False
            params = data.split("\r\n")
            print(data)
            userMessage = ''
            for i in messages:
                if i[0] == params[1]:
                    userMessage = userMessage + f'  {i[0]}:{i[1]}  ||'
            if userMessage != '':
                print(f"your messages {userMessage}")
                if session_id == False or session not in auth_users:
                    send_response(client, 500, "Please log in.")
                
                else:
                    send_response(client, 200, userMessage)
            else:
                send_response(client, 210, 'You have no messages!')
                
                
        elif 'CLEAR' in data:
            if 'session' in data:
                session = data.split('session:')[1].split('\r\n')[0]
                print(session)
            else:
                session = False
            params = data.split("\r\n")
            print(data)
            x = 0
            if messages != []:
                if session_id == False or session not in auth_users:
                    send_response(client, 500, "Please log in.")

                else:
                    #TODO: czemu nie działa for i???
                    print(messages)
                    while x<1:
                        print('1')
                        if 1==1:
                            x=x+1
                            print('2')
                        print('3')
                    print('4')
                    for i in messages:
                        print(i)
                        if i[0] == params[1]:
                            messages.pop(x)
                        x = x+1
                    send_response(client, 200, 'Messages deleted!')
            else:
                send_response(client, 210, 'You have no messages to delete!')
            

    client.close()


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ip_connection)
    s.listen(5)

    try:
        while True:
            client, addr = s.accept()
            print("CONNECTED WITH ", addr[0])
            start_new_thread(server_client, (client, ))
    except KeyboardInterrupt:
        s.close()
