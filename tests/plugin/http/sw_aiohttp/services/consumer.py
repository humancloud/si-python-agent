#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
import time

import aiohttp
from aiohttp import web


async def handle(request):
    name = request.match_info.get('name', 'Anonymous')

    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://user:pass@provider:9091/{name}') as response:
            time.sleep(.5)
            json = await response.json()
            return web.Response(text=str(json))


app = web.Application()
app.add_routes([web.get('/', handle), web.get('/{name}', handle)])

if __name__ == '__main__':
    web.run_app(app, port=9090)
