import socket
import cv2
import pickle
import struct
import imutils



server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 8081
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen(5)

print("LISTENING AT:",socket_address)
n=input("Create the Password: ")
lst=['shubham.varma@somaiya.edu']
print(lst)
while True:
    print("\nPress 1 to add new member to the organization\nPress 2 to remove a member from the orginization\nPress 3 to start the operation")
    member=int(input("Enter your choice: "))
    if member==1:
        new_member=input("Enter the Email ID of the member: ")   
        lst.append(new_member)
        print(lst)
    elif member==2:
        del_member=input("Enter the Email ID of the member: ")
        try:
            lst.remove(del_member)
            print(lst)
        except :
            print("\nThe Email ID id not registered in the orginization")
            continue
    elif member==3:
        print("Wating for connection...")
        try:
            while True:
                 
                client_socket,addr = server_socket.accept()
                b=client_socket.recv(1024).decode()
                check_email=client_socket.recv(1024).decode()
                lst = set(lst)
                print('GOT CONNECTION FROM:',addr)
                if check_email in lst :
                    if b==n:
                        client_socket.send(bytes('\n\twelcome to the live fotage\n','utf-8'))
                        if client_socket:
                            cam = cv2.VideoCapture(0)
        
                            while(cam.isOpened()):
                                ret,frame1=cam.read()
                                cv2.putText(frame1, 'TKR-R2', (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
                                frame1 = imutils.resize(frame1,width=800)
                                a = pickle.dumps(frame1)
                                message= struct.pack("Q",len(a))+a
                                client_socket.sendall(message)
                                # cv2.imshow('Live cam feed',frame1)
                                if cv2.waitKey(1) == ord('q'):
                                    client_socket.close()
                                            
                    else:
                        client_socket.send(bytes('\n\tAcess denied\n','utf-8'))
                        print("Closed Connection for:",addr,"(Reason: Entered wrong passcode)")
                        client_socket.close()
                else:
                    client_socket.send(bytes('\n\tAcess denied\n','utf-8'))
                    print("Closed Connection for:",addr,"(Reason: Email address does NOT belong to the orginization)")
                    client_socket.close()
        except:
            print("An existing connection was forcibly closed by the remote host")
            continue
        