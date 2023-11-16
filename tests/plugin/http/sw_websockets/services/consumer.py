#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
from websockets.client import connect

import asyncio

if __name__ == '__main__':
    from fastapi import FastAPI
    import uvicorn

    app = FastAPI()

    @app.get('/ws')
    async def websocket_ping():
        async with connect('ws://provider:9091/ws', extra_headers=None) as websocket:
            await websocket.send('Ping')

            response = await websocket.recv()
            await asyncio.sleep(0.5)

            await websocket.close()
            return response

    uvicorn.run(app, host='0.0.0.0', port=9090)
