import socket
import cv2
import pickle
import keyboard as key

HOST = '127.0.0.1'
PORT = 65432

data = b""

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST,PORT))
        s.sendall(b'successful connection')
        data = s.recv(786597)
        img = pickle.loads(data)
        cv2.imshow("img",img)
        cv2.waitKey(0)
        #object size for (521,512 img)
        while True:
            try:
                if key.is_pressed('space'):
                    s.sendall(b'request img') 
                    data = s.recv(786597)
                    img = pickle.loads(data)
                elif key.is_pressed('q'):
                    break
            except:
                print("other key")
                break
            cv2.imshow("img",img)
            cv2.waitKey(0)   
except:
    print('connection closed')
