#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

"""
This module contains the Consumer part of the e2e tests.
consumer (FastAPI) -> consumer (AIOHTTP) -> provider (FastAPI + logging_with_exception)

ASGI, used by Gunicorn and normal test
"""
import aiohttp
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/artist-consumer')
@app.post('/artist-consumer')
async def application():
    try:
        payload = {}
        async with aiohttp.ClientSession() as session:
            async with session.post('http://provider:9090/artist-provider', data=payload) as response:
                return await response.json()
    except Exception as e:  # noqa
        return {'message': str(e)}


if __name__ == '__main__':
    # noinspection PyTypeChecker
    uvicorn.run(app, host='0.0.0.0', port=9090)
