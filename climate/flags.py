# Copyright (c) 2013 Leif Johnson <leif@leifjohnson.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

'''Useful utilities for command-line arguments.'''

import argparse
import plac


class Parser(argparse.ArgumentParser):
    '''This class provides some sane default command-line argument behaviors.

    In particular, the help formatter includes default values, and arguments can
    be loaded from files. Files can contain arguments in two ways: one per line,
    or many-per-line. For one-per-line arguments, spaces etc. are preserved,
    while for many-per-line arguments, the line must start with a dash, and
    multiple arguments are split on whitespace. In all cases, shell-style
    comments are removed from the file before processing.
    '''

    SANE_DEFAULTS = dict(
        fromfile_prefix_chars='@',
        conflict_handler='resolve',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    def __init__(self, *args, **kwargs):
        kw = {}
        kw.update(Parser.SANE_DEFAULTS)
        kw.update(kwargs)
        super(Parser, self).__init__(*args, **kw)

    def convert_arg_line_to_args(self, line):
        '''Remove # comments and blank lines from arg files.'''
        S = '__@__'
        line = line.replace(r'\#', S).split('#')[0].strip().replace(S, '#')
        if line:
            if line[0] == '-' and ' ' in line:
                for p in line.split():
                    yield p
            else:
                yield line


_ARGS = None
_CMDS = None

def _get_args():
    '''Enable arguments through the Python argparse module.'''
    global _ARGS
    if not _ARGS:
        _ARGS = Parser()
    return _ARGS

def _get_commands():
    '''Enable sub-parsers of command line arguments.'''
    global _CMDS
    if not _CMDS:
        _CMDS = _get_args().add_subparsers(dest='command_name')
    return _CMDS

# from http://stackoverflow.com/questions/5376837
def _is_running_in_ipython():
    '''Return True iff the runtime environment is provided by IPython.'''
    try:
        __IPYTHON__
        return True
    except NameError:
        return False


def add_mutex_arg_group(*args, **kwargs):
    '''Add a mutually-exclusive argparse group.

    Returns
    -------
    A mutually-exclusive argparse argument group object.
    '''
    return _get_args().add_mutually_exclusive_group(*args, **kwargs)


def add_arg_group(*args, **kwargs):
    '''Add an argparse argument group.

    Returns
    -------
    An argparse argument group object.
    '''
    return _get_args().add_argument_group(*args, **kwargs)


def add_arg(*args, **kwargs):
    '''Add an argparse argument.'''
    return _get_args().add_argument(*args, **kwargs)


def add_command(*args, **kwargs):
    '''Add an argparse command parser.

    The name of the command will be stored in the "command_name" argparse
    variable.

    Returns
    -------
    An argparse command parser object.
    '''
    return _get_commands().add_parser(*args, **kwargs)


def parse_args(**overrides):
    '''Parse command-line arguments, overriding with keyword arguments.

    Returns
    -------
    args :
        The command-line argument namespace object.
    kwargs :
        A dictionary version of the command-line arguments.
    '''
    args = argparse.Namespace()
    if not _is_running_in_ipython():
        args = _get_args().parse_args()
    for k, v in overrides.items():
        setattr(args, k, v)
    return args, vars(args)

def annotate(*args, **kwargs):
    '''Return a decorator for plac-style argument annotations.'''
    return plac.annotations(*args, **kwargs)
