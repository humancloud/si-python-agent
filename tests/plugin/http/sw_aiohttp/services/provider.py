#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from aiohttp import web


async def handle(request):
    name = request.match_info.get('name', 'Anonymous')
    return web.json_response({
        name: name,
    })


app = web.Application()
app.add_routes([web.get('/', handle), web.get('/{name}', handle)])

if __name__ == '__main__':
    web.run_app(app, port=9091)
