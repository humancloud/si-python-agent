#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
import requests
from websockets.client import connect

import asyncio

if __name__ == '__main__':
    from fastapi import FastAPI
    import uvicorn

    app = FastAPI()

    @app.get('/users')
    async def application():
        res = requests.get('http://provider:9091/users', timeout=5)
        websocket_pong = await websocket_ping()
        return {'http': res.json(), 'websocket': websocket_pong}

    async def websocket_ping():
        async with connect('ws://provider:9091/ws', extra_headers=None) as websocket:
            await websocket.send('Ping')

            response = await websocket.recv()
            await asyncio.sleep(0.5)

            await websocket.close()
            return response

    uvicorn.run(app, host='0.0.0.0', port=9090)
