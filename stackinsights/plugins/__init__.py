#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
import inspect
import logging
import pkgutil
import re
import traceback

import pkg_resources
from packaging import version

import stackinsights
from stackinsights import config
from stackinsights.loggings import logger
from stackinsights.utils.comparator import operators
from stackinsights.utils.exception import VersionRuleException


def install():
    disable_patterns = config.agent_disable_plugins
    if isinstance(disable_patterns, str):
        disable_patterns = [re.compile(p.strip()) for p in disable_patterns.split(',') if p.strip()]
    else:
        disable_patterns = [re.compile(p.strip()) for p in disable_patterns if p.strip()]
    for importer, modname, _ispkg in pkgutil.iter_modules(stackinsights.plugins.__path__):
        if any(pattern.match(modname) for pattern in disable_patterns):
            logger.info("plugin %s is disabled and thus won't be installed", modname)
            continue
        logger.debug('installing plugin %s', modname)
        plugin = importer.find_module(modname).load_module(modname)

        # todo: refactor the version checker, currently it doesn't really work as intended
        supported = pkg_version_check(plugin)
        if not supported:
            logger.debug("check version for plugin %s's corresponding package failed, thus "
                         "won't be installed", modname)
            continue

        if not hasattr(plugin, 'install') or inspect.ismethod(plugin.install):
            logger.warning("no `install` method in plugin %s, thus the plugin won't be installed", modname)
            continue

        # noinspection PyBroadException
        try:
            plugin.install()
            logger.debug('Successfully installed plugin %s', modname)
        except Exception:
            logger.warning(
                'Plugin %s failed to install, please ignore this warning '
                'if the package is not used in your application.',
                modname
            )
            traceback.print_exc() if logger.isEnabledFor(logging.DEBUG) else None


def pkg_version_check(plugin):
    supported = True

    # no version rules was set, no checks
    if not hasattr(plugin, 'version_rule'):
        return supported

    pkg_name = plugin.version_rule.get('name')
    rules = plugin.version_rule.get('rules')

    try:
        current_pkg_version = pkg_resources.get_distribution(pkg_name).version
    except pkg_resources.DistributionNotFound:
        # when failed to get the version, we consider it as supported.
        return supported

    current_version = version.parse(current_pkg_version)
    # pass one rule in rules (OR)
    for rule in rules:
        if rule.find(' ') == -1:
            if check(rule, current_version):
                return supported
        else:
            # have to pass all rule_uint in this rule (AND)
            rule_units = rule.split(' ')
            results = [check(unit, current_version) for unit in rule_units]
            if False in results:
                # check failed, try to check next rule
                continue
            else:
                return supported

    supported = False
    return supported


def check(rule_unit, current_version):
    idx = 2 if rule_unit[1] == '=' else 1
    symbol = rule_unit[0:idx]
    expect_pkg_version = rule_unit[idx:]

    expect_version = version.parse(expect_pkg_version)
    f = operators.get(symbol) or None
    if not f:
        raise VersionRuleException(f'version rule {rule_unit} error. only allow >,>=,==,<=,<,!= symbols')

    return f(current_version, expect_version)
