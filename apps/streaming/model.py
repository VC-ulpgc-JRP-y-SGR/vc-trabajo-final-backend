import socket
import cv2
import numpy as np
import socket
import pickle

class NetworkCamera:
    def __init__(self, ip, port, buffer_size) -> None:
        self.ip = ip
        self.port = port
        self.buffer_size = buffer_size

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
    
    def close(self):
        self.sock.close()
    
    def _receive_frame(self):
        try:
            self.connect()
            size_data = self.sock.recv(4)
            size = int.from_bytes(size_data, byteorder='big')
            data = b''
            while len(data) < size:
                packet = self.sock.recv(self.buffer_size)
                if not packet: break
                data += packet

            frame = pickle.loads(data)
            self.close()
            return cv2.imdecode(frame, cv2.IMREAD_COLOR)
        except:
            return np.zeros((480, 640, 3), dtype=np.uint8)
    
    def get_frame(self):
        img = self._receive_frame()
        img = cv2.resize(img, (640, 480))
        ret, jpeg = cv2.imencode('.jpg', img)
        frame = jpeg.tobytes()
        return frame
    
    def generator(self):
        while True:
            frame = self.get_frame()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
