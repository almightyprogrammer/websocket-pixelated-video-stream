import asyncio
import cv2
import numpy as np
from websockets.asyncio.server import serve

async def handle_client(websocket):
    try:
        async for data in websocket:
            np_data = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
            if frame is not None:
                cv2.imshow("Server Received Frame", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        cv2.destroyAllWindows()

async def main():
    async with serve(handle_client, "localhost", 8765):
        print("Server running on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())


