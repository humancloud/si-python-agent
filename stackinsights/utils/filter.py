#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import re
import traceback
from urllib.parse import urlparse

from stackinsights import config


def sw_urlparse(url):
    # Removes basic auth credentials from netloc
    url_param = urlparse(url)
    safe_netloc = url_param.netloc
    try:
        safe_netloc = f"{url_param.hostname}{f':{str(url_param.port)}' if url_param.port else ''}"
    except ValueError:  # illegal url, skip
        pass

    return url_param._replace(netloc=safe_netloc)


def sw_filter(target: str):
    # Remove user:pw from any valid full urls
    # this filter is disabled by default due to perf impact
    if config.agent_log_reporter_safe_mode:
        return re.sub(r'://(.*?)@', r'://', target)
    return target


def sw_traceback():
    stack_trace = traceback.format_exc(limit=config.agent_cause_exception_depth)

    return sw_filter(target=stack_trace)
