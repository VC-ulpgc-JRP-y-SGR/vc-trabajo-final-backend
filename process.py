import ctypes
import cv2
import multiprocessing as mp
import numpy as np
import time
import ctypes

video = cv2.VideoCapture(0)
ret, frame = video.read()
shape = frame.shape

def numpy_to_shared(arr):
    shared_array = mp.Array(ctypes.c_double, arr.size)
    return shared_array

def shared_to_numpy(shared_array, shape):
    arr = np.frombuffer(shared_array.get_obj())
    reshaped_arr = arr.reshape(shape)
    return reshaped_arr

def fill_shared_array_with_numpy(shared_array, numpy_arr):
    reshaped_numpy_arr = numpy_arr.reshape(-1)
    shared_array[:] = reshaped_numpy_arr[:]

def process1(shared_array, q):
    while True:  # Run for 5 iterations
        if not q.empty():
            frame = q.get()
            print(frame)

def process2(shared_array, q):
    video = cv2.VideoCapture(0)

    while True:
        frame = np.random.rand(*shape)
        q.put(frame)
        time.sleep(1)

if __name__ == "__main__":
    shared_array = numpy_to_shared(np.zeros(shape))
    queue = mp.Queue()

    p1 = mp.Process(target=process1, args=(shared_array, queue))
    p2 = mp.Process(target=process2, args=(shared_array, queue))

    p1.start()
    p2.start()

    p1.join()
    p2.join()
