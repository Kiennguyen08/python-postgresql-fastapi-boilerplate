import asyncio
import json
import random
from datetime import datetime, timedelta

import websockets


async def client_simulator(client_id: str):
    async with websockets.connect(
        f"ws://localhost:7000/api/v1/minitest/chat/ws/{client_id}?timezone=Asia/Ho_Chi_Minh"
    ) as ws:
        try:
            # Send 10 messages over 5 minutes
            start = datetime.now()
            for _ in range(100):
                await asyncio.sleep(random.uniform(0, 2))  # Spread over 5 mins

                msg_type = random.choice(["text", "voice", "video"])
                message = {
                    "type": msg_type,
                    "content": f"{msg_type} message from {client_id}",
                    "timestamp": datetime.now().isoformat(),
                }
                await ws.send(json.dumps(message))
        except Exception as e:
            print(f"Client {client_id} error: {e}")


async def main():
    tasks = [client_simulator(f"client_{i}") for i in range(100)]
    # tasks = [client_simulator("client_t") for i in range(100)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
