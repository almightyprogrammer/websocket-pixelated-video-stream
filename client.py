#!/usr/bin/env python

"""Client using the asyncio API."""

import cv2
import asyncio
from websockets.asyncio.client import connect


def pixelate(image, pixel_size=10):
    h = image.shape[0]
    w = image.shape[1]
    small = cv2.resize(image, (w // pixel_size, h // pixel_size), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)

async def send_frames():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    async with connect("ws://localhost:8765") as websockets:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Missed a frame...")
            
            frame = pixelate(frame, 10)
            _, buffer = cv2.imencode('.jpg', frame)
            await websockets.send(buffer.tobytes())
            await asyncio.sleep(0.01)
    
asyncio.run(send_frames())
            





async def hello():
    async with connect("ws://localhost:8765") as websocket:
        await websocket.send("Hello world!")
        message = await websocket.recv()
        print(message)


asyncio.run(hello())