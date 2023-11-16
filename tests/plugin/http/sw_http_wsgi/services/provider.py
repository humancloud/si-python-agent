#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import time


if __name__ == '__main__':
    from werkzeug import Request, Response

    @Request.application
    def application(request):
        time.sleep(0.5)
        return Response('{"song": "Despacito", "artist": "Luis Fonsi"}')

    from werkzeug.serving import run_simple

    PORT = 9091
    run_simple('', PORT, application)
