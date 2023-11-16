#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import sys

import requests
from django.conf import settings
from django.conf.urls import url
from django.http import JsonResponse

settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
)


def index(request):
    res = requests.post('http://provider:9091/users', timeout=5)
    return JsonResponse(res.json())


urlpatterns = (
    url('users', index),
)


if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
