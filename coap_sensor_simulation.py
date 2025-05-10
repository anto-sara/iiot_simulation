import asyncio
import random
from aiocoap import *

async def simulate_sensor_data():
    protocol = await Context.create_client_context()
    while True:
        temperature = random.uniform(20.0, 25.0)
        humidity = random.uniform(30.0, 50.0)
        payload = f'{{"temperature": {temperature}, "humidity": {humidity}}}'.encode('utf-8')
        request = Message(code=POST, payload=payload)
        request.set_request_uri('coap://localhost/sensor/data')
        try:
            response = await protocol.request(request).response
            print(f"CoAP - Sent: {payload.decode('utf-8')}")
        except Exception as e:
            print(f"Failed to send CoAP message: {e}")
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(simulate_sensor_data())