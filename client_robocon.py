import socket
import cv2
import pickle
import struct
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# host_ip = '192.168.137.52'
host_ip = '192.168.137.212'
port = 8081
client_socket.connect((host_ip,port)) 
password=input("Enter the Password: ")
Email=input("Enter the Listed Email-ID: ")
client_socket.send(bytes(password,'utf-8'))
client_socket.send(bytes(Email,'utf-8'))
print(client_socket.recv(1024).decode())
data = b""
payload_size = struct.calcsize("Q")
while True:
	while len(data) < payload_size:
		packet = client_socket.recv(4*1024) 
		if not packet: break
		data+=packet
	packed_msg_size = data[:payload_size]
	data = data[payload_size:]
	msg_size = struct.unpack("Q",packed_msg_size)[0]
	
	while len(data) < msg_size:
		data += client_socket.recv(4*1024)
	frame_data = data[:msg_size]
	data  = data[msg_size:]
	frame = pickle.loads(frame_data)
	aaaa= cv2.resize(frame, (1080,720))
	bbbb=cv2.circle(aaaa, (540,400), 10, (255, 0, 0), -1)
	cv2.imshow("RECEIVING live cam feed",bbbb)
	# cv2.imshow("RECEIVING live cam feed_1",frame)
	key = cv2.waitKey(1) & 0xFF
	if key  == ord('q'):
		break
client_socket.close()