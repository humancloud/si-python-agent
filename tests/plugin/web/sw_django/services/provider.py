#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import sys
import time

from django.conf import settings
from django.conf.urls import url
from django.http import JsonResponse

settings.configure(
    DEBUG=True,
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
)


def index(request):
    time.sleep(0.5)
    return JsonResponse({'song': 'Despacito', 'artist': 'Luis Fonsi'})


urlpatterns = (
    url('users', index),
)


if __name__ == '__main__':
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
