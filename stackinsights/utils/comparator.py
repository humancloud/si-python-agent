#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

operators = {
    '<': lambda cv, ev: cv < ev,
    '<=': lambda cv, ev: cv < ev or cv == ev,
    '==': lambda cv, ev: cv == ev,
    '>=': lambda cv, ev: cv > ev or cv == ev,
    '>': lambda cv, ev: cv > ev,
    '!=': lambda cv, ev: cv != ev
}
