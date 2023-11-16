#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
import requests

if __name__ == '__main__':
    from fastapi import FastAPI
    import uvicorn

    app = FastAPI()


    @app.get('/users')
    async def application():
        res = requests.get('http://provider:9091/users', timeout=5)
        return {'http': res.json()}


    uvicorn.run(app, host='0.0.0.0', port=9090)
