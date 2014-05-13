# -*- coding: utf-8 -*-
"""
    utils.py

    :copyright: (c) 2014 by Aravinda VK
    :license: BSD, see LICENSE for more details.
"""

import subprocess
import xml.etree.cElementTree as etree
from glusterfsrest.exceptions import GlusterCliFailure, GlusterCliBadXml
from glusterfsrest.exceptions import ParseError


def execute(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, env=None, close_fds=True):
    p = subprocess.Popen(cmd,
                         stdin=stdin,
                         stdout=stdout,
                         stderr=stderr,
                         env=env,
                         close_fds=close_fds)

    (out, err) = p.communicate()
    return (p.returncode, out, err)


def statuszerotrue(func):
    def wrapper(*args, **kwargs):
        cmd = func(*args, **kwargs)
        rc, _, err = execute(cmd + ['--xml'])
        if rc == 0:
            return True

        return GlusterCliFailure(err)

    return wrapper


def execute_and_output(cmd, func):
    rc, out, err = execute(cmd + ['--xml'])
    if rc == 0:
        return func(out)

    return GlusterCliFailure(rc, err)


def checkxmlcorrupt(xmldata):
    try:
        return etree.fromstring(xmldata)
    except (ParseError, AttributeError, ValueError) as e:
        raise GlusterCliBadXml(str(e))
