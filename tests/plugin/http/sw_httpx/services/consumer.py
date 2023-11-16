#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import uvicorn
from fastapi import FastAPI
import httpx

async_client = httpx.AsyncClient()
client = httpx.Client()
app = FastAPI()


@app.post('/users')
async def application():
    try:
        await async_client.post('http://provider:9091/users')
        res = client.post('http://provider:9091/users')

        return res.json()
    except Exception:  # noqa
        return {'message': 'Error'}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9090)
