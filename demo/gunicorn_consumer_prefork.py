#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
"""
This one demos how to use gunicorn with a simple fastapi uvicorn app.
"""
import logging

from fastapi import FastAPI

"""
# Run this to see sw-python working with gunicorn
sw-python -d run -p \
    gunicorn gunicorn_consumer_prefork:app \
    --workers 2 --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8088
"""

app = FastAPI()


@app.get('/cat')
async def application():
    try:
        logging.critical('fun cat got a request')
        return {'Cat Fun Fact': 'Fact is cat, cat is fat'}
    except Exception as e:  # noqa
        return {'message': str(e)}


if __name__ == '__main__':
    # noinspection PyTypeChecker
    # uvicorn.run(app, host='0.0.0.0', port=8088)
    ...
