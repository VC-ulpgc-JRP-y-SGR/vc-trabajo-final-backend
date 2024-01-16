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
        self.sock = None
        self.last_frame = None

    def connect(self):
        if self.sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.ip, self.port))
    
    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
    
    def _receive_frame(self):
        try:
            self.connect()
            size_data = self.sock.recv(4)
            if not size_data:
                raise ConnectionError("Failed to receive frame size")
            size = int.from_bytes(size_data, byteorder='big')
            data = b''
            while len(data) < size:
                packet = self.sock.recv(self.buffer_size)
                if not packet: break
                data += packet

            frame = pickle.loads(data)
            self.last_frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            return cv2.imdecode(frame, cv2.IMREAD_COLOR)
        except Exception as e:
            print(f"Error receiving frame: {e}")
            self.close()
            if self.last_frame is not None:
                return self.last_frame
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
